# -*- coding: cp1250 -*-
import os
from inspect import getsourcefile

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

#==============================================================================
# PATHS
#path='Segmentation_Images'
vol = 1 #1 for VOL1, or 2 for VOL2
#data_folder = 'C:\Users\Virneal\Documents\GitHub\KidneySegmentation\InputData' + str(vol) #folder with the images (I think we should handle VOL1 and VOL2 separately)
data_folder = 'ProjectData\\Segmentation_Images\\VOL' + str(vol) #folder with the images (I think we should handle VOL1 and VOL2 separately)
output_folder ='OutputData' #folder with the output images

current_file_dir = os.path.dirname(os.path.abspath(getsourcefile(lambda:0))) #find current file path
parent_dir = os.path.normpath(os.path.join(current_file_dir, "..")) # go up one level
data_path = os.path.join(parent_dir, data_folder) #absolute path to the data
output_path = os.path.join(parent_dir, output_folder)

os.chdir(current_file_dir)
import auxiliary_functions as aux
#==============================================================================

for niifilename in os.listdir(data_path):

    Loaded_File = nib.load(os.path.join(data_path, niifilename))
    Data_from_file = Loaded_File.get_data()
    print(niifilename)
    Data_max = np.max(np.abs(Data_from_file))
    if Data_max !=0: Data_from_file = Data_from_file / Data_max #normalisation - get rid of the 1 vs 222 problem
    
    if 'Merged_Segmentation' not in locals():
        Data_shape = Data_from_file.shape
        Merged_Segmentation = Data_from_file
    else:
        #Merged_Segmentation = Merged_Segmentation + Data_from_file #shows overlaps, but in the end we should use the one below
        Merged_Segmentation = np.maximum(Merged_Segmentation, Data_from_file) #should do the same job as the triple loop
        
# plot merging results
aux.show_slices([Merged_Segmentation[:,:,7], Merged_Segmentation[:,:,14], Merged_Segmentation[:,:,21]])
aux.slicer(Merged_Segmentation)


# Create Nifti Image object and save
Merged_Segmentation_nifti = nib.Nifti1Image(Merged_Segmentation, Loaded_File.affine)
os.chdir(output_path) #change the path to the output folder for saving
outputfname = 'Kidney_Mask_VOL' + str(vol) + '.nii'
nib.save(Merged_Segmentation_nifti, outputfname) #musisz mieć obiekt Nifti, żeby zapisać przez nib
# jeśli dobrze rozumiem, potrzebujemy Kindey_Mask_VOL1 do działania na obrazkach z VOL1 i drugiego pliku Kidney_Mask_VOL2 dla VOL2