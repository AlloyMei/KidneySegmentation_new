#2. Create time course vectors

time_course_vector_name = 'time_course_vector_' + kidney_mask_side + '.npy'

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
TCV_pure_idx = np.where(TCV_all[:,0]!=0)[0] # indices of nonzero-TCV voxels
TCV_pure = TCV_all[TCV_pure_idx,:] # nonzero-TCV voxels

kmeans = KMeans(n_clusters=3).fit(time_course_vector)

kmeans_TCV = KMeans(n_clusters=3).fit(TCV_pure)


time_course_vector_dict = {}
for label in np.unique(kmeans.labels_):
    time_course_vector_dict[label] = time_course_vector[kmeans.labels_==label,:]
aux.plot_averaged_TCV(time_course_vector_dict)

TCV_dict = {}
for label in np.unique(kmeans_TCV.labels_):
    TCV_dict[label] = TCV_pure[kmeans_TCV.labels_==label,:]
aux.plot_averaged_TCV(TCV_dict)
