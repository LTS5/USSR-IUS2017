import os
from ius.utils import reconstruct_image
import sys

if len(sys.argv) < 2:
    processing_unit = 'CPU'
else:
    processing_unit = sys.argv[1]

# Data paths
list_data_path = ['data/picmus16/carotid_cross_expe_dataset_rf.hdf5', 'data/picmus17/dataset_rf_numerical_transmission_1_nbPW_1.hdf5', 'data/picmus17/dataset_rf_numerical_transmission_1_nbPW_5.hdf5']

# DAS
results_path = os.path.join('results','das')
selected_indexes = [[37], [35, 36, 37, 38, 39]]
for dpath in list_data_path:
    if '_expe_' in dpath:
        for index in selected_indexes:
            reconstruct_image('DAS', dpath, results_path, selected_indexes=index, processing_unit=processing_unit)
    else:
        reconstruct_image('DAS', dpath, results_path, processing_unit=processing_unit)

# FISTA - SA
list_data_path_1pw = ['data/picmus16/carotid_cross_expe_dataset_rf.hdf5', 'data/picmus17/dataset_rf_numerical_transmission_1_nbPW_1.hdf5']
results_path = 'results/FISTA'
list_regularization_parameter = [7e-4, 3e-4]
for dpath, regularization_parameter in zip(list_data_path_1pw, list_regularization_parameter):
    reconstruct_image('FISTA', dpath, results_path, regularization_parameter=regularization_parameter, processing_unit=processing_unit)

# FISTA - LP
results_path = 'results/FISTALP'
list_regularization_parameter = [3e-2, 1e-3]
for dpath, regularization_parameter in zip(list_data_path_1pw, list_regularization_parameter):
    reconstruct_image('FISTALP', dpath, results_path, regularization_parameter=regularization_parameter, processing_unit=processing_unit)