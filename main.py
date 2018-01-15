# KIDNEY SEGMENTATION PROJECT - main.py

# imports here
import os
from inspect import getsourcefile

import auxiliary_functions as aux

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
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

labels_fn = 'kmeans_labels_' + kidney_mask_side + '.npy'

# Plotting kidney with a slicer enabled
kidney_frozen_fig = aux.slicer(MaskedData[50,:,:,:], slideaxis=2, title='Kidney at 50s, coronal view')
kidney_fixedslice_fig = aux.slicer(MaskedData[:,:,:,21], slideaxis=0, title='Kidney at coronal slice 21 of 30')

#==============================================================================

#2. create time course vector - reshape to 2D = 1*spatial + 1*TCV
# (-> 2D array of shape (number_of_voxels, length_of_TCV) )
# By 'flattennig' the last 3 dimensions to 1
TCV_all = np.transpose(MaskedData).reshape(-1, MaskedData.shape[0])

#TCV_all - for all voxels, also those outside the kidney
# transpose to change the order of the dimensions - first dimension (time) becomes last
# then we can use reshape with -1 as the first arguments
# - to flatten along all dimensions but the last one (time)

"""
#==============================================================================
#3. PCA
# reduce dimensionality of the set (from 74 to n_components)
pca = PCA(n_components=15, whiten=False).fit(TCV_all)
TCV_red = pca.transform(TCV_all)

#==============================================================================
#4. K-Means
# -> k.means_labels - 1D array of length of 'number_of_voxels',
# filled with values: 0, 1, 2, 3 - cluster indices for each voxel;
# one of the labels - for non-kidney voxels

kmeans = KMeans(n_clusters=4).fit(TCV_red)
kmeans_labels = kmeans.labels_
np.save(labels_fn, kmeans_labels)
"""

kmeans_labels = np.load(labels_fn)
#==============================================================================
#5. Find groups of voxels belonging to each cluster (0, 1, 2, 3);
# TCV_dict[0] - all time course vectors classified to cluster 0

TCV_dict = {}
for label in np.unique(kmeans_labels):
    TCV_dict[label] = TCV_all[kmeans_labels==label,:]


# plot averaged intensity changes (averaged time course vector) for each cluster
aux.plot_averaged_TCV(TCV_dict)

#==============================================================================
#6. Find the 3D positions of the point groups
# in the original (3D) data;
kidney_segmented = np.transpose(np.array(kmeans_labels).reshape(np.transpose(MaskedData).shape[:-1]))

if kidney_mask_side == 'R':
    kidney_medulla = np.where(kidney_segmented==1,1,0)
    kidney_pelvis = np.where(kidney_segmented==2,1,0)
    kidney_cortex = np.where(kidney_segmented==3,1,0)
else:
    kidney_medulla = np.where(kidney_segmented==1,1,0)
    kidney_cortex = np.where(kidney_segmented==2,1,0)
    kidney_pelvis = np.where(kidney_segmented==3,1,0)

segmented_plot = aux.slicer(kidney_segmented, slideaxis=2, title='Segmented')

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

Loaded_File = nib.load(os.path.join(input_path, 'Output volume_1.nii'))
aff = Loaded_File.affine

Cortex_nifti = nib.Nifti1Image(kidney_cortex, aff)
Medulla_nifti = nib.Nifti1Image(kidney_medulla, aff)
Pelvis_nifti = nib.Nifti1Image(kidney_pelvis, aff)

fnameend = '_VOL' + str(vol) + '.nii'
os.chdir(output_path) #change the path to the output folder for saving
nib.save(Cortex_nifti, 'Cortex'+fnameend)
nib.save(Medulla_nifti, 'Medulla'+fnameend)
nib.save(Pelvis_nifti, 'Pelvis'+fnameend)