import os

# range(start,stop,step) : Can do "steps" with the third parameter (currently 1) 2nd number (stop) is NOT included, so usually add 1.
# Numbers should be one-based (matching MATLAB, filenames, etc.)

input_directory="data"
output_directory="data"

filename_cost_video=os.path.join( input_directory,"COST_rawvideo.avi" )
filename_shifts=os.path.join( input_directory,"shifts_all.mat" )

filename_stabilized_video=os.path.join( output_directory, "COST_rotvideo.avi" )
filename_stabilized_avg=os.path.join( output_directory, "COST_rotavg.tif" )


## Settings inside WSL (Windows subsystem for Linux) ##

# volume_directory="/mnt/f/Torsion_correction_data/Image_00001_AO001R_896_512_600_50_1.57_12000_-ve0.13_Nd0.0_20ms/registervol_combine"
# volumes=os.path.join( volume_directory,'*','*registeredvol.mat')
#volumes_rotated_directory="/mnt/f/Torsion_correction_data/Image_00001_AO001R_896_512_600_50_1.57_12000_-ve0.13_Nd0.0_20ms/torsion_fixed_cropped"

#volume_directory=r"/mnt/f/Torsion_correction_data/Image_00001_AO001R_896_512_600_50_1.57_12000_-ve0.13_Nd0.0_20ms/registervol_combine_padded"
#volumes=os.path.join( volume_directory,'*registeredvol.mat')
#volumes_rotated_directory="/mnt/f/Torsion_correction_data/Image_00001_AO001R_896_512_600_50_1.57_12000_-ve0.13_Nd0.0_20ms/torsion_fixed_padded"

## Settings inside Windows shell

volume_directory=r"F:\Torsion_correction_data\Image_00001_AO001R_896_512_600_50_1.57_12000_-ve0.13_Nd0.0_20ms\registervol_combine_padded"
volumes=os.path.join( volume_directory,'*registeredvol.mat')
volumes_rotated_directory=r"F:\Torsion_correction_data\Image_00001_AO001R_896_512_600_50_1.57_12000_-ve0.13_Nd0.0_20ms\torsion_fixed_padded"

padding_pixels_each_side=50
volume_rot90=1

# Optional:
volumes_to_process=range(1,500,1)  # Can specify a subset. Okay if larger than data.5
layers_to_process=range(13,18) # Z-planes. others are left as zero
filename_transforms=os.path.join( output_directory, "xform_info.pickle" )
do_rot90=0 # Rotate the COST video, since it's rot90 from the raw volumes. Don't use yet.
stabilized_unrot90=0
