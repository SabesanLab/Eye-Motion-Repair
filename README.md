## Eye Motion Repair.
Code that removes residual distortions due to eye motion from images and videos processed by Demotion.
The correction algorithm was developed (and forked here) from Rob Cooper's Lab, and tweaked to be able to process entire directories of AOOCT images for Sabesan Lab. The analysis code uses the SimpleITK library to learn arbitrary affine transformations vs. a reference image. The algorithm arbitrarily chooses a reference image near the center with minimal motion.

### Steps:
1. Make files needed for torsion analysis
   - Generate the COST movie and shifts file
   - Note the directory that contains the movie and the shifts. (Currently the shifts file may need tweaking.)
2. Edit the "torsion_params.py" in the same directory as Python program.
   - For now, especially the directory/filenames of the input (COST movie and shifts file)
   - What the shift dimensions look like
   - Specify where the program should save the computed shifts/rotations
3. Run the program with the "compute" option.
   - It will go through each frame of the movie and learn a 2D affine transformation matrix for each frame, based on a (guessed, with minimal shifts) reference
4. Run the program with the "apply" option
   - Specify the directory(ies) where the raw volumes are -- can use wildcards if volumes are in multiple folders.
   - Specify the directory to output the rotated volumes (all go in a single folder)
   - The program will go through each volume (and each axial layer sequentially) and apply the 2D transformation matrix
