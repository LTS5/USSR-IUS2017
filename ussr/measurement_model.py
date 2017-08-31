class MeasurementModel:

    # Constructor
    def __init__(self,
                 interpolation='cubic',
                 obliquity=True,
                 propagation=True,
                 pulse=True):

        # Interpolation type
        valid_interp = ('linear', 'nearest', 'cubic')
        if isinstance(interpolation, str):
            if interpolation in valid_interp:
                self.__interpolation = interpolation
            else:
                NotImplementedError('Interpolation method {} not implemented')
        else:
            raise TypeError('interpolation argument must be a str, valid types: {valid}.'.format(
                valid=', '.join(valid_interp)
            ))

        # Obliquity factor
        if isinstance(obliquity, bool):
            self.__obliquity = obliquity
        else:
            raise TypeError('obliquity argument must be a bool')

        # Propagation factor
        if isinstance(propagation, bool):
            self.__propagation = propagation
        else:
            raise TypeError('propagation argument must be a bool')

        # Pulse
        if isinstance(pulse, bool):
            self.__pulse = pulse
        else:
            raise TypeError('pulse argument must be a bool')

    # Properties
    @property
    def interpolation(self):
        return self.__interpolation

    @property
    def obliquity(self):
        return self.__obliquity

    @property
    def propagation(self):
        return self.__propagation

    @property
    def pulse(self):
        return self.__pulse
