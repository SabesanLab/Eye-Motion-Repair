import pickle
import numpy as np
import os
import SimpleITK as sitk
import scipy.io as sio
import glob

def do_apply(torsion_params):
    file=open(torsion_params.filename_transforms,'rb')
    xform_info=pickle.load(file)

    print( 'Input is in: %s'%torsion_params.volume_directory)

    filename1=glob.glob(torsion_params.volumes)[0]
    vol1=sio.loadmat(filename1)['registered_vol']
    print('Volumes have shape: '+str(vol1.shape))

    shape_compute=xform_info['shape']

    if all ((not(torsion_params.volume_rot90),shape_compute[0]==vol1.shape[1]-torsion_params.padding_pixels_each_side*2,
             shape_compute[1]==vol1.shape[2]-torsion_params.padding_pixels_each_side*2)):
        flip_volumes=False
    elif all ((torsion_params.volume_rot90,shape_compute[0]==vol1.shape[2]-torsion_params.padding_pixels_each_side*2,
               shape_compute[1]==vol1.shape[1]-torsion_params.padding_pixels_each_side*2)):
        flip_volumes=True
        print ("Volume rot90 needed. Computed shape="+str(shape_compute))
    else:
        print("Computed shape="+str(shape_compute)+', rot90 not specified. Cannot determine. Stopping.')
        print("To do rot90 of volumes, set volume_rot90=1 in params file.")
        sys.exit()
        
    shifted=np.zeros( vol1.shape, dtype='complex')
    avg_im=np.zeros( vol1.shape )
    avg_nonzero_count=np.zeros(vol1.shape)

    if not(os.path.exists(torsion_params.volumes_rotated_directory )):
        os.mkdir( torsion_params.volumes_rotated_directory )

    for vol_file in glob.glob(torsion_params.volumes):
        nvol = int( vol_file.split('/')[-1].split('_')[0] )
        if (torsion_params.volumes_to_process is not None) and (nvol not in torsion_params.volumes_to_process):
            continue
        
        print( '\nVolume %02d -'%nvol,end=' ')
        
        vol1=sio.loadmat(vol_file)['registered_vol']
        xform1=xform_info["xforms"][nvol-1] # 0 based to 1-based:TODO, maybe switch to all one-based ?
        
        for nlayer in torsion_params.layers_to_process:
            print( nlayer, end=' ')
            
            layer1=vol1[nlayer,:,:]
            realpart=np.abs(layer1)
            imagpart=np.angle(layer1)
            
            if flip_volumes:
                realpart = np.flipud( np.rot90(realpart) )
                imagpart = np.flipud( np.rot90(imagpart) )

            if torsion_params.padding_pixels_each_side>0:
                cx,cy=xform1.GetCenter()
                cx += torsion_params.padding_pixels_each_side
                cy += torsion_params.padding_pixels_each_side
                xform1.SetCenter((cx,cy))
            
            out_im = sitk.Resample(sitk.GetImageFromArray(realpart), xform1, sitk.sitkLanczosWindowedSinc)
            out_im_arr = np.reshape( out_im, np.array(shape_compute[0:2])+torsion_params.padding_pixels_each_side*2)
            
            if flip_volumes:
                out_im_arr = np.rot90( np.flipud( out_im_arr), -1 )
                
            avg_im[nlayer] += out_im_arr
            avg_nonzero_count[nlayer] += (out_im_arr > 0)
            
            out_complex = sitk.Resample(sitk.GetImageFromArray(imagpart), xform1, sitk.sitkLanczosWindowedSinc)
            out_complex = np.reshape( out_complex, np.array(shape_compute[0:2])+torsion_params.padding_pixels_each_side*2 )
            
            if flip_volumes:
                out_complex = np.rot90( np.flipud( out_complex), -1 )
            
            shifted[nlayer] = out_im_arr + 1j * out_complex
        
        # Save all rotated layers in new reg_vol file
        newname=os.path.join(torsion_params.volumes_rotated_directory,'%d_registeredvol.mat'%nvol)
        sio.savemat(newname,{'registered_vol':shifted})
        
        # Overwrite average image each volume to monitor progress
        newavg=os.path.join(torsion_params.volumes_rotated_directory,'avg_volume.mat')
        # Prevent divide by zero. If all frames are 0, total will be zero, so /1 is good. Using inf/nans also works.
        av_count_now=avg_nonzero_count+(avg_nonzero_count==0)*1
        sio.savemat(newavg, {'avg_volume':avg_im/av_count_now} )

    print( '\n\nOutput is in: %s'%torsion_params.volumes_rotated_directory)

