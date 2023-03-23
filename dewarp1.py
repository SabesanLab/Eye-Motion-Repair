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
    filename_ref=sys.argv[-3]
    filename_target=sys.argv[-2]
    filename_xf=sys.argv[-1]
    
    ref=io.loadmat(filename_ref)['data']
    target=io.loadmat(filename_target)['data']

    shifted = np.zeros( (np.shape(ref)[0], np.shape(ref)[1], 2));
    print (np.shape(shifted))
    
    shifted[...,0]=ref
    shifted[...,1]=target

    # Determine and remove residual torsion.
    mask_data = (shifted>0).astype("float32")
    shifted, xforms, inliers, itk_xforms = optimizer_stack_align(shifted, mask_data,
                                                        reference_idx=0)
   
    io.savemat(filename_xf, {'xforms':xforms})
    
        
