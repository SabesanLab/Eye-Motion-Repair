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
    file_ref=sys.argv[-2]
    file_target=sys.argv[-1]
    print("in=",file_ref)
    print("out=",file_target)
      
    shifted = np.zeros( 2, size(file_ref)[0], size(file_ref)[1]);
    
    ref=io.loadmat(file_ref)
    target=io.loadmat(file_target)
    
    # Determine and remove residual torsion.
    mask_data = (shifted>0).astype("float32")
    shifted, xforms, inliers, itk_xforms = optimizer_stack_align(shifted, mask_data,
                                                        reference_idx=reference_frame_idx)
   
    save_video(torsion_params.filename_stabilized_video,(shifted*255).astype("uint8"),30 )

    # Clamp our data.
    mask_data[mask_data < 0] = 0
    mask_data[mask_data >= 1] = 1
    
    io.savemat('xf1.mat', {'xforms':xforms})
    
        overlap_map, sum_map = weighted_z_projection(mask_data, mask_data)
        avg_im, sum_map = weighted_z_projection(shifted, mask_data)
    
        cv2.imwrite(torsion_params.filename_stabilized_avg, (avg_im*255).astype("uint8"))
        #im_conf = Image.fromarray((avg_im * 255).astype("uint8"), "L")
        #im_conf.putalpha(Image.fromarray((overlap_map * 255).astype("uint8"), "L"))
        #im_conf.save("M:\\Dropbox (Personal)\\Research\\Torsion_Distortion_Correction\\COST_rawvideo_reavg.png")
        #im_conf.save("data/COST_rawvideo_reavg.png")

    if do_apply:
        torsion_apply.do_apply(torsion_params)
        
