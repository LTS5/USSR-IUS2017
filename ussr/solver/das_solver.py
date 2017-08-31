from ussr.solver.solver_base import SolverBase
from ussr.measurement_model import MeasurementModel


class DAS(SolverBase):
    # Constructor
    def __init__(self,
                 sequence):

        # Solver name
        name = 'DAS'

        # Measurement model for DAS
        measurement_model = MeasurementModel(interpolation='cubic',
                                             obliquity=True,
                                             propagation=False,
                                             pulse=False)

        # Super constructor
        super(DAS, self).__init__(name=name,
                                  measurement_model=measurement_model,
                                  sequence=sequence)
