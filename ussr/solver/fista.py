from ussr.solver.solver_base import SolverBase


class FISTA(SolverBase):
    # Constructor
    def __init__(self,
                 measurement_model,
                 sequence,
                 prior,
                 regularization_parameter,
                 max_iter=1e2):

        # Solver name
        name = 'FISTA'

        # Super constructor
        super(FISTA, self).__init__(name=name,
                                    measurement_model=measurement_model,
                                    sequence=sequence)

        # Prior type
        valid_prior = ('SA', 'lp')
        if prior in valid_prior:
            self.__prior = prior
        else:
            raise NotImplementedError('Prior {used} not implemented, valid priors: {valid}'.format(
                used=prior, valid=', '.join(valid_prior)
            ))

        # Regularization param
        if isinstance(regularization_parameter, float):
            self.__regularization_parameter = regularization_parameter
        else:
            raise TypeError('Regularization parameter must be a float')

        # Max iter
        self.__max_iter = int(max_iter)
        # if isinstance(max_iter, float):
        #     self.__max_iter = max_iter
        # else:
        #     raise TypeError('Maximum number of iterations parameter must be a int')


    # Properties
    @property
    def prior(self):
        return self.__prior

    @property
    def regularization_parameter(self):
        return self.__regularization_parameter

    @property
    def max_iter(self):
        return self.__max_iter
