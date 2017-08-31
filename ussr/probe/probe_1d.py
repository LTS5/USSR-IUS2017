import numpy as np
import scipy.signal


class Probe1D:
    def __init__(self,
                 name,
                 pitch,
                 center_frequency,
                 element_number,
                 element_width=None,
                 element_height=None,
                 bandwidth=None,
                 impulse_cycles=None,
                 impulse_window=None):

        self.__type = '1D'
        self.__name = name
        self.__pitch = pitch
        self.__center_frequency = center_frequency
        self.__element_number = element_number
        self.__element_width = element_width if element_width is not None else pitch
        self.__element_height = element_height
        self.__bandwidth = bandwidth
        self.__impulse_cycles = impulse_cycles
        self.__impulse_window = impulse_window

    # Properties
    @property
    def pitch(self):
        return self.__pitch

    @property
    def center_frequency(self):
        return self.__center_frequency

    @property
    def element_number(self):
        return self.__element_number

    @property
    def element_width(self):
        return self.__element_width

    @property
    def element_height(self):
        return self.__element_height

    @property
    def bandwidth(self):
        return self.__bandwidth

    @property
    def impulse_cycles(self):
        return self.__impulse_cycles

    @property
    def impulse_window(self):
        return self.__impulse_window

    #   Computed properties
    @property
    def width(self):
        return (self.element_number - 1) * self.pitch

    @property
    def element_positions(self):
        return np.linspace(start=-self.width / 2, stop=self.width / 2, num=self.element_number)

    # Methods
    def impulse_response(self, sampling_frequency):
        dt = 1 / sampling_frequency
        if self.impulse_window in ['hanning', 'blackman']:
            t_start = 0
            t_stop = int(self.impulse_cycles / self.center_frequency * sampling_frequency) * dt  # int() applies floor
            t_num = int(self.impulse_cycles / self.center_frequency * sampling_frequency) + 1  # int() applies floor
            # t_stop_old = self.impulse_cycles / self.center_frequency
            # t = np.arange(t_start, t_stop_old, dt)
            t = np.linspace(t_start, t_stop, t_num)
            impulse = np.sin(2 * np.pi * self.center_frequency * t)
            if self.impulse_window == 'hanning':
                win = np.hanning(impulse.shape[0])
            elif self.impulse_window == 'blackman':
                win = np.blackman(impulse.shape[0])
            else:
                raise NotImplementedError('Window type {} not implemented'.format(self.impulse_window))
            return impulse * win
        elif self.impulse_window == 'gauss':
            # Compute cutoff time for when the pulse amplitude falls below `tpr` (in dB) which is set at -100dB
            tpr = -60
            t_cuttoff = scipy.signal.gausspulse('cutoff', fc=self.center_frequency, bw=self.bandwidth, tpr=tpr)
            t = np.arange(-t_cuttoff, t_cuttoff, dt)
            return scipy.signal.gausspulse(t, fc=self.center_frequency, bw=self.bandwidth, tpr=tpr)
        else:
            raise NotImplementedError('Window type {} not implemented'.format(self.impulse_window))
