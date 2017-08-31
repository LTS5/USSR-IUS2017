from ussr.sequence import USSequence
from ussr.measurement_model import MeasurementModel
from ussr.solver.interface import Interface


class SolverBase:
    # Constructor
    def __init__(self,
                 name,
                 measurement_model,
                 sequence):

        # Solver type
        if isinstance(name, str):
            self.__name = name
        else:
            raise TypeError('solver_type argument must be a str.')

        # Measurement model
        if isinstance(measurement_model, MeasurementModel):
            self.__measurement_model = measurement_model
        else:
            raise TypeError('measurement_model argument must be a MeasurementModel')

        # Sequence
        if isinstance(sequence, USSequence):
            self.__sequence = sequence
        else:
            raise TypeError('sequence argument must be a USSequence')

    # Properties
    @property
    def name(self):
        return self.__name

    @property
    def measurement_model(self):
        return self.__measurement_model

    @property
    def sequence(self):
        return self.__sequence

    # Methods
    def reconstruct_image(self, processing_unit=None):
        interface = Interface(self)
        return interface.launch(processing_unit=processing_unit)

    def benchmark(self, processing_unit=None, run_number=10):
        interface = Interface(self)
        return interface.launch(processing_unit=processing_unit, run_number=run_number)
