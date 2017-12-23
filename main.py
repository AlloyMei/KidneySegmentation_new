# KIDNEY SEGMENTATION PROJECT - main.py

# imports here
import os
from inspect import getsourcefile

import auxiliary_functions as aux

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
plt.close('all')

#==============================================================================
# PATHS
#path='Segmentation_Images'
vol = '1' # 1 or 2 But we will probably work on 1 only

data_folder = 'InputData\\VOL_' + vol #folder with the images (I think we should handle VOL1 and VOL2 separately)
output_folder = 'OutputData\\O_VOL_' + vol #folder with the output images

current_file_dir = os.path.dirname(os.path.abspath(getsourcefile(lambda:0))) #find current file path
parent_dir = os.path.normpath(os.path.join(current_file_dir, "..")) # go up one level
input_path = os.path.join(parent_dir, data_folder) #absolute path to the data
output_path = os.path.join(parent_dir, output_folder)
mask_path = os.path.join(parent_dir, 'MaskData')

os.chdir(current_file_dir)
#==============================================================================
#1. load the data
kidney_mask_side = 'L' # L or R
masked_output_fn = 'Masked_' + kidney_mask_side + '.nii'
MaskedData = nib.load(os.path.join(output_path, masked_output_fn))
MaskedData = np.array(MaskedData.get_data())

time_course_vector_name = 'time_course_vector_' + kidney_mask_side + '.npy'

# Plotting kidney with a slicer enabled
kidney_frozen_fig = aux.slicer(MaskedData[50,:,:,:], slideaxis=2, title='Kidney at 50s, coronal view')
kidney_fixedslice_fig = aux.slicer(MaskedData[:,:,:,21], slideaxis=0, title='Kidney at coronal slice 21 of 30')


#==============================================================================
#2. Create time course vectors

"""
col_number = 0

for i in range(MaskedData.shape[1]):
    for j in range(MaskedData.shape[2]):
        for k in range(MaskedData.shape[3]):
            if MaskedData[0,i,j,k]!=0:
                col_number=col_number+1
print col_number
time_course_vector = np.zeros(MaskedData.shape[0]*col_number).reshape(MaskedData.shape[0],col_number)
print np.shape(time_course_vector)

counter = 1
for a in range(MaskedData.shape[0]):
    print(counter)
    temp = []
    for i in range(MaskedData.shape[1]):
        for j in range(MaskedData.shape[2]):
            for k in range(MaskedData.shape[3]):
                if MaskedData[a,i,j,k]!=0:
                    temp.append(MaskedData[a,i,j,k])
    if(len(temp)!=col_number):
        while(len(temp)<col_number):
            temp.append(0)
    temp1 = np.asarray(temp)
    time_course_vector[a,:]=temp1
    counter=counter+1

# Saving time course vector for left and right kidney to files to avoid re-calculation
os.chdir(output_path) #change the path to the output folder for saving
np.save(time_course_vector_name, np.transpose(time_course_vector))
os.chdir(current_file_dir)
"""
# Load time course vector
time_course_vector = np.load(os.path.join(output_path, time_course_vector_name))
#"""

# druga wersja TCV - przez reshape
TCV_all = MaskedData.reshape(-1, MaskedData.shape[0]) #all voxels
TCV_pure_idx = np.where(TCV_all[:,0]!=0)[0] # indices of nonzero-TCV voxels
TCV_pure = TCV_all[TCV_pure_idx,:] # nonzero-TCV voxels

#==============================================================================
#3. reshape to 2D = 1*spatial + 1*TCV
# (-> 2D array of shape (number_of_voxels, length_of_TCV) )
# method? By 'flattennig' the first 3 dimensions to 1?

#update: 3. already in 2.?

#==============================================================================
#4. K-Means
# -> k.means_labels - 1D array of length of 'number_of_voxels',
# filled with values: 0, 1, 2 - cluster indices for each voxel;
# plot the K-Means - scatter plot


kmeans = KMeans(n_clusters=3).fit(time_course_vector)
kmeans_TCV = KMeans(n_clusters=3).fit(TCV_pure)


#==============================================================================
#5. Find groups of voxels belonging to each cluster (0, 1, 2);
# plot averaged intensity changes for each group
time_course_vector_dict = {}
for label in np.unique(kmeans.labels_):
    time_course_vector_dict[label] = time_course_vector[kmeans.labels_==label,:]
aux.plot_averaged_TCV(time_course_vector_dict)

TCV_dict = {}
for label in np.unique(kmeans.labels_):
    TCV_dict[label] = TCV_pure[kmeans_TCV.labels_==label,:]
aux.plot_averaged_TCV(TCV_dict)

#==============================================================================
#6. Find the 3D positions of the point groups
# in the original (3D) data;
# create ROIs - 3 separate 3D images (spatial only)
# and maybe an additional image - 3 colours of labels
# superimposed on the original image?
# Like with the brain in the 4th semester
# CortexData = KidneyData
# MedullaData = KidneyData
# PelvisData = KidneyData
#
# #==============================================================================
# #7. save to Nifti
