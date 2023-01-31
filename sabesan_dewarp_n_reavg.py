import pathlib

import cv2
import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
from scipy import io
from PIL.Image import Image

from ocvl.preprocessing.improc import optimizer_stack_align, weighted_z_projection
from ocvl.utility.resources import load_video,save_video
import pickle,sys,os

import importlib.machinery, importlib.util

import torsion_apply 

# "compute"=Compute the transforms from the COST movie, generate new COST movie and its avg.
# "apply"=Apply transforms from file specified in params file to volumes
# "both=First compute then apply.
mode="both" # compute|apply|both

if __name__ == "__main__":
    # TODO: process params
    do_compute=True
    do_apply=True
    filename_params="torsion_params.py"

    if "apply" in sys.argv:
        do_compute=False
        do_apply=True
    elif "compute" in sys.argv:
        do_compute=True
        do_apply=False

    print("Using params file '%s'"%filename_params)
    print("Use 'apply' or 'compute' for partial execution. Default is to do both operations, based on params file.") 

    loader = importlib.machinery.SourceFileLoader('torsion_params', filename_params)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    torsion_params = importlib.util.module_from_spec(spec)
    loader.exec_module(torsion_params)
       
    if do_compute:

        if not(os.path.exists(torsion_params.output_directory )):
                os.mkdir( torsion_params.output_directory )

        # Load our video data.
        res = load_video(torsion_params.filename_cost_video)
        num_frames = res.data.shape[-1]
        width = res.data.shape[1]
        height = res.data.shape[0]
        video_data = res.data.astype("float32") / 255
        print( "Movie width,height: %02d,%02d"%  (width, height ) )
    
        matcontents = io.loadmat(torsion_params.filename_shifts)
    
        all_shifts = matcontents["shifts_all"]
    
        all_shifts = np.zeros((height, 2, num_frames))
        for f in range(num_frames):
            all_shifts[..., f] = matcontents["shifts_all"][f * height:(f + 1) * height, :]
    
        median_col_shifts = np.nanmedian(all_shifts[:, 0, :], axis=-1)
        median_row_shifts = np.nanmedian(all_shifts[:, 1, :], axis=-1)
    
        col_base = np.tile(np.arange(width, dtype=np.float32)[np.newaxis, :], [height, 1])
        row_base = np.tile(np.arange(height, dtype=np.float32)[:, np.newaxis], [1, width])
    
        shifted = np.zeros(video_data.shape)
    
        # Best guess for reference frame, since we can't tell from the data.
        reference_frame_idx = np.sum(np.sum(np.abs(all_shifts) < 2, axis=0), axis=0).argmax()
    
        print( "Reference Idx: %03d"%reference_frame_idx )
    
        for f in range(num_frames):
            print('Reshifting frame %03d/%03d'%(f,num_frames), end=' ') # Don't make new lines so can see some of the debug info
            colshifts = all_shifts[:, 0, f] - median_col_shifts
            rowshifts = all_shifts[:, 1, f] - median_row_shifts
    
            centered_col_shifts = col_base - np.tile(colshifts[:, np.newaxis], [1, width]).astype("float32")
            centered_row_shifts = row_base - np.tile(rowshifts[:, np.newaxis], [1, width]).astype("float32")
    
            shifted1 = cv2.remap(video_data[..., f], centered_col_shifts, centered_row_shifts,
                                        interpolation=cv2.INTER_CUBIC)
    
            if torsion_params.do_rot90:
                shifted[..., f] = np.flipud( np.rot90( shifted1, -1) )
            else:
                shifted[..., f] = shifted1
    
            #plt.figure(0)
            #plt.clf()
            #plt.imshow(shifted[..., f])
            #plt.show(block=False)
            #plt.pause(0.01)
    
        # Determine and remove residual torsion.
        mask_data = (shifted>0).astype("float32")
        shifted, xforms, inliers, itk_xforms = optimizer_stack_align(shifted, mask_data,
                                                            reference_idx=reference_frame_idx)
    
        #if torsion_params.outv
    
        save_video(torsion_params.filename_stabilized_video,(shifted*255).astype("uint8"),30 )
    
        # Clamp our data.
        mask_data[mask_data < 0] = 0
        mask_data[mask_data >= 1] = 1
    
        with open(torsion_params.filename_transforms, 'wb') as handle:
            dict_info={'xforms':itk_xforms,'ref_idx':reference_frame_idx,
                    'shape':video_data.shape,'rot90':torsion_params.do_rot90}
            pickle.dump(dict_info,handle)
    
        overlap_map, sum_map = weighted_z_projection(mask_data, mask_data)
        avg_im, sum_map = weighted_z_projection(shifted, mask_data)
    
        cv2.imwrite(torsion_params.filename_stabilized_avg, (avg_im*255).astype("uint8"))
        #im_conf = Image.fromarray((avg_im * 255).astype("uint8"), "L")
        #im_conf.putalpha(Image.fromarray((overlap_map * 255).astype("uint8"), "L"))
        #im_conf.save("M:\\Dropbox (Personal)\\Research\\Torsion_Distortion_Correction\\COST_rawvideo_reavg.png")
        #im_conf.save("data/COST_rawvideo_reavg.png")

    if do_apply:
        torsion_apply.do_apply(torsion_params)
        
