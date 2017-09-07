import numpy as np
from .us_sequence import USSequence


class PWSequence(USSequence):
    def __init__(self,
                 name,
                 probe,
                 sampling_frequency,
                 transmit_frequency,
                 transmit_wave,
                 transmit_cycles,
                 mean_sound_speed,
                 medium_attenuation,
                 angles,
                 initial_times,
                 data):

        sequence_type = 'PW'

        super(PWSequence, self).__init__(name=name,
                                         sequence_type=sequence_type,
                                         probe=probe,
                                         sampling_frequency=sampling_frequency,
                                         transmit_frequency=transmit_frequency,
                                         transmit_wave=transmit_wave,
                                         transmit_cycles=transmit_cycles,
                                         mean_sound_speed=mean_sound_speed,
                                         medium_attenuation=medium_attenuation,
                                         initial_times=initial_times,
                                         data=data)

        self.__angles = angles

    # Properties
    @property
    def angles(self):
        return self.__angles

    @property
    def image_limits(self):
        x_min = -self.probe.width / 2
        x_max = self.probe.width / 2

        # Image limits are computed assuming a normal incidence PW (even if zero angle is not available)
        ind_zero_angle_check = np.where(self.angles == 0)[0]
        if ind_zero_angle_check.size == 0:
            ind_angle = 0
        else:
            ind_angle = int(ind_zero_angle_check)  # lists require int or slice for indexing

        initial_time = self.initial_times[ind_angle]

        sample_number = self.sample_numbers[ind_angle]

        z_min = initial_time * self.mean_sound_speed / 2
        z_max = (initial_time + sample_number * 1 / self.sampling_frequency) * self.mean_sound_speed / 2

        return [[x_min, x_max], [z_min, z_max]]

