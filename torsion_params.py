import os

input_directory="../data"
output_directory="../data"

filename_cost_video=os.path.join( input_directory,"COST_rawvideo.avi" )
video_do_rot90=0
filename_shifts=os.path.join( input_directory,"shifts_all.mat" )

filename_stabilized_video=os.path.join( output_directory, "COST_rotvideo.avi" )
filename_stabilized_avg=os.path.join( output_directory, "COST_rotavg.tif" )
stabilized_unrot90=0

filename_transforms=os.path.join( output_directory, "xforms_itk.pickle" )
