import numpy as np
import scipy.signal
from abc import ABCMeta, abstractmethod

from ussr.probe import Probe1D


class USSequence(metaclass=ABCMeta):
    def __init__(self,
                 name,
                 sequence_type,
                 probe,
                 sampling_frequency,
                 transmit_frequency,
                 transmit_wave,
                 transmit_cycles,
                 mean_sound_speed,
                 medium_attenuation,
                 initial_times,
                 data):

        self.__name = name
        self.__type = sequence_type
        # TODO: generalize to other probes
        if isinstance(probe, Probe1D):
            self.__probe = probe
        else:
            raise TypeError('`probe` must be an instance of class `Probe`')
        self.__sampling_frequency = sampling_frequency
        self.__transmit_frequency = transmit_frequency
        self.__transmit_wave = transmit_wave
        self.__transmit_cycles = transmit_cycles
        self.__mean_sound_speed = mean_sound_speed
        self.__medium_attenuation = medium_attenuation
        self.__initial_times = initial_times
        self.__data = data

    # Properties
    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    @property
    def probe(self):
        return self.__probe

    @property
    def sampling_frequency(self):
        return self.__sampling_frequency

    @property
    def transmit_frequency(self):
        return self.__transmit_frequency

    @property
    def transmit_wave(self):
        return self.__transmit_wave

    @property
    def transmit_cycles(self):
        return self.__transmit_cycles

    @property
    def transmit_cycles(self):
        return self.__transmit_cycles

    @property
    def mean_sound_speed(self):
        return self.__mean_sound_speed

    @property
    def medium_attenuation(self):
        return self.__medium_attenuation

    @property
    def initial_times(self):
        return self.__initial_times

    @initial_times.setter
    # TODO: add len check (based on a `size` attribute of the sequence, e.g. angles in PW)
    def initial_times(self, initial_times):
        if isinstance(initial_times, (list, tuple)):
            self.__initial_times = initial_times
        else:
            raise TypeError

    @property
    def data(self):
        return self.__data

    @data.setter
    # TODO: add len check (based on a `size` attribute of the sequence, e.g. angles in PW)
    def data(self, data):
        if isinstance(data, (list, tuple)):
            self.__data = data
        else:
            raise TypeError

    # Additional properties
    @property
    def wavelength(self):
        return self.mean_sound_speed / self.probe.center_frequency

    @property
    @abstractmethod
    def image_limits(self): pass

    @property
    def sample_numbers(self):
        return [d.shape[1] for d in self.data]

    # Methods
    def estimate_received_pulse(self):
        # Electric excitation
        dt = 1 / self.sampling_frequency
        t_start = 0
        t_stop = int(self.transmit_cycles / self.transmit_frequency * self.sampling_frequency) * dt  # int() applies floor
        t_num = int(self.transmit_cycles / self.transmit_frequency * self.sampling_frequency) + 1  # int() applies floor
        # t_stop_old = self.impulse_cycles / self.center_frequency
        # t = np.arange(t_start, t_stop_old, dt)
        t = np.linspace(t_start, t_stop, t_num)

        if self.transmit_wave == 'sine':
            excitation = np.sin(2 * np.pi * self.transmit_frequency * t)
        elif self.transmit_wave == 'square':
            excitation = scipy.signal.square(2 * np.pi * self.transmit_frequency * t)
        else:
            raise NotImplementedError('Transmit wave type {} not implemented'.format(self.transmit_wave))

        # Received pulse
        impulse_response = self.probe.impulse_response(sampling_frequency=self.sampling_frequency)
        pulse = np.convolve(np.convolve(excitation, impulse_response), impulse_response)

        # Normalize
        pulse /= pulse.max()

        return pulse

    def normalize_data(self):
        # TODO: should the normalization be performed on the entire set?
        for data in self.data:
            data /= data.max()

    def _tgc_exp_factor(self):
        # Convert `alpha` to SI units, i.e. in Np/Hz/m
        db_to_neper = 1 / (20 * np.log10(np.exp(1)))
        m_to_cm = 1e-2
        hz_to_mhz = 1e6
        alpha_si = self.medium_attenuation * db_to_neper / hz_to_mhz / m_to_cm

        gain = []
        for initial_time, data in zip(self.initial_times, self.data):
            sample_number = data.shape[-1]
            depth = initial_time * self.mean_sound_speed / 2 + np.arange(
                sample_number) * self.mean_sound_speed / (2 * self.sampling_frequency)
            # TODO: center_frequency or transmit_frequency???
            gain.append(np.exp(2 * alpha_si * self.probe.center_frequency * depth))  # roundtrip

        return gain

    def apply_tgc(self):
        tgc_factors = self._tgc_exp_factor()
        for tgc_fact, data in zip(tgc_factors, self.data):
            data *= tgc_fact

    def crop_data(self, first_index, last_index):
        """
        Crop data
        :param first_index: int or array-like (i.e. iterable)
        :param last_index: int or array-like (i.e. iterable)
        :return: 
        """
        array_types = (list, tuple, np.ndarray)
        if not isinstance(first_index, (int, *array_types)):
            raise TypeError('first_index must be an int or an array-like')
        if not isinstance(last_index, (int, list, tuple, np.ndarray)):
            raise TypeError('last_index must be an int or an array-like')
        if isinstance(first_index, int):
            first_indexes = [first_index for _ in range(len(self.data))]
        elif isinstance(first_index, array_types):
            first_indexes = first_index
        else:
            raise TypeError
        if isinstance(last_index, int):
            last_indexes = [last_index for _ in range(len(self.data))]
        elif isinstance(last_index, array_types):
            last_indexes = last_index
        else:
            raise TypeError

        # Loop over data and initial times
        data_crop = []
        initial_times_update = []
        for data, init_time, f_ind, l_ind in zip(self.data, self.initial_times, first_indexes, last_indexes):
            data_crop.append(data[:, first_index:last_index])
            initial_times_update.append(init_time + first_index * 1 / self.sampling_frequency)

        # Set data and corresponding initial_times
        self.data = data_crop
        self.initial_times = initial_times_update
