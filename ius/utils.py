# TO ADD if example script launched from USSR/examples/python
import ussr.data.picmus as picmus_data
from ussr.measurement_model import MeasurementModel
from ussr.solver import FISTA, DAS
import ussr.utils.matlab as matlab


def reconstruct_image(solver, data_path, results_path, selected_indexes=[37], regularization_parameter=0.0, max_iter=200, processing_unit='CPU'):
    # Load PICMUS data
    if '_expe_' in data_path:
        seq = picmus_data.import_sequence(data_path, remove_tgc=True, selected_indexes=selected_indexes)
        seq.apply_tgc()
    elif '_in_vitro_' in data_path:
        seq = picmus_data.import_sequence(data_path, remove_tgc=True)
        seq.apply_tgc()
    else:
        seq = picmus_data.import_sequence(data_path, remove_tgc=False)

    # Normalize the data
    seq.normalize_data()

    # Reconstruct image
    print('************ Reconstructing "{}" ************ '.format(seq.name))

    # Define the solver
    if solver is 'DAS':
        solver = DAS(sequence=seq)

    elif solver is 'FISTA':
        measurement_model = MeasurementModel(interpolation='cubic',
                                             obliquity=True,
                                             propagation=True,
                                             pulse=True)
        solver = FISTA(measurement_model=measurement_model,
                       sequence=seq,
                       prior='SA',
                       regularization_parameter=regularization_parameter,
                       max_iter=max_iter)
    else:
        measurement_model = MeasurementModel(interpolation='cubic',
                                             obliquity=True,
                                             propagation=True,
                                             pulse=True)
        solver = FISTA(measurement_model=measurement_model,
                       sequence=seq,
                       prior='lp',
                       regularization_parameter=regularization_parameter,
                       max_iter=max_iter)

    rf_image = solver.reconstruct_image(processing_unit=processing_unit)

    # Export the results
    matlab.export(results_path, rf_image, seq)

