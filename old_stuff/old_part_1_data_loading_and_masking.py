"""

kidney_mask_side = 'L' # L or R
maskfname = '02_VOL1_KID_' + kidney_mask_side + '.nii'
KidneyMask = nib.load(os.path.join(mask_path, maskfname)).get_data()

# load the registration data (4D = 3*spatial + 1*temporal)
for niifilename in sorted(os.listdir(input_path), key=len):
    if niifilename[:2] != '._':
        Loaded_File = nib.load(os.path.join(input_path, niifilename))
        Data_from_file = Loaded_File.get_data()
        print(niifilename)
        
        if 'KidneyData' not in locals():
            Data_shape = Data_from_file.shape
            KidneyData = Data_from_file.reshape(tuple([1L]) + Data_shape)
        else:
            KidneyData = np.concatenate((Data_from_file.reshape(tuple([1L]+list(Data_shape))), KidneyData), axis=0)
            # time at axis=0

#print("'KidneyData' array shape: %s, size: %d" %(KidneyData.shape, KidneyData.size))

# impose the mask on the 4D image
KidneyMaskTile = np.tile(KidneyMask,(KidneyData.shape[0],1,1,1))
KidneyData = KidneyData * KidneyMaskTile

# Plotting kidney with a slicer enabled
#kidney_frozen_fig = aux.slicer(KidneyData[50,:,:,:], slideaxis=2, title='Kidney at 50s, coronal view')
#kidney_fixedslice_fig = aux.slicer(KidneyData[:,:,:,21], slideaxis=0, title='Kidney at coronal slice 21 of 30')

#save to Nifti
aff = Loaded_File.affine
MaskedData = nib.Nifti1Image(KidneyData, aff)
os.chdir(output_path) #change the path to the output folder for saving
masked_output_fn = 'Masked_' + kidney_mask_side + '.nii'
nib.save(MaskedData, masked_output_fn)
os.chdir(current_file_dir)
"""

# part 7 - save to nifti
# aff = Loaded_File.affine
# Cortex_nifti = nib.Nifti1Image(CortexData, aff)
# Medulla_nifti = nib.Nifti1Image(MedullaData, aff)
# Pelvis_nifti = nib.Nifti1Image(PelvisData, aff)
#
# fnameend = '_VOL' + kidney_mask_side + '.nii'
# os.chdir(output_path) #change the path to the output folder for saving
# nib.save(Cortex_nifti, 'Cortex'+fnameend)
# nib.save(Medulla_nifti, 'Medulla'+fnameend)
# nib.save(Cortex_nifti, 'Pelvis'+fnameend)
# print('ROIs saved to %s' %output_path)



