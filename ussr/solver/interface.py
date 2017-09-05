import os
import shutil
import numpy as np
import subprocess
import ussr.solver
import ussr.sequence
import ussr.utils.ui


class Interface:
    # Constructor
    def __init__(self, solver):
        # Input and output folders
        #   Set paths relative to the location USSR_BASE_PATH found relatively to the file interface.py
        USSR_BASE_PATH = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
        self.__tmp_folder = os.path.join(USSR_BASE_PATH, '.tmp')

        # Binaries folders
        self.__gpu_bin_path = os.path.join(USSR_BASE_PATH, 'bin', 'ussr_gpu')
        self.__cpu_bin_path = os.path.join(USSR_BASE_PATH, 'bin', 'ussr_cpu')
        self.__use_gpu = False

        # Solver properties
        """
        TODO: if `solver` parameter is called, then it looses its reference to the SolverBase class...
        Ex:
        solver.sequence  <- will work
        solver.measurement_model <- cannot find ref since already call before...
        Hence a `tmp_solver` is created...
        Seems to be a PyCharm error...
        """
        tmp_solver = solver
        if not isinstance(tmp_solver, ussr.solver.SolverBase):
            raise TypeError('solver attribute must be an instance of {base_class}'.format(
                base_class=ussr.solver.SolverBase.__name__))

        # Private dictionary settings
        settings = dict()

        # Solver
        """
        Solver keys:
            solver:
            max_iter: not required for DAS
            transform: not required (only when using prior SA)
            gamma: not required (only PDFB)
            beta: not required (only PDFB)
            mu: not required (only FISTA, FISTALP)
        """

        if isinstance(tmp_solver, ussr.solver.DAS):
            settings['solver'] = 'DAS'
        elif isinstance(tmp_solver, ussr.solver.FISTA):
            if tmp_solver.prior == 'SA':
                settings['solver'] = 'FISTA'
                settings['transform'] = 'SARA'
            elif tmp_solver.prior == 'lp':
                settings['solver'] = 'FISTALP'
            settings['max_iter'] = int(tmp_solver.max_iter)
            settings['mu'] = tmp_solver.regularization_parameter
        else:
            raise NotImplementedError('Solver {name} not supported'.format(name=tmp_solver.name))

        #   Additional default settings
        settings['verbose'] = 0
        settings['nb_runs'] = 1
        settings['input_folder'] = self.input_folder
        settings['output_folder'] = self.output_folder
        settings['processing_unit'] = 'CPU'

        # Sequence
        # TODO: generalize for other Sequence types
        seq = tmp_solver.sequence
        if isinstance(seq, ussr.sequence.PWSequence):
            settings['transmit_wave'] = 'PW'

            # Angles
            angles_deg = np.rad2deg(seq.angles)
            # angles_deg = seq.angles
            angles_str_list = ['{:.6f}'.format(angle) for angle in angles_deg]
            angles_str = ' '.join(angles_str_list)
            settings['angles'] = angles_str
            settings['nb_transmit_waves'] = len(seq.angles)

            # Additional required fields not related to PW
            settings['zn'] = 0
            settings['xn'] = 0
        else:
            raise NotImplementedError('Sequence {name} not supported'.format(name=seq.name))

        settings['sound_speed'] = seq.mean_sound_speed
        settings['central_frequency'] = seq.probe.center_frequency
        settings['pitch'] = seq.probe.pitch
        settings['nb_elements'] = float(seq.probe.element_number)
        settings['nb_active'] = float(seq.probe.element_number)
        settings['sampling_frequency'] = seq.sampling_frequency
        settings['wavelength'] = seq.wavelength
        settings['dx'] = settings['pitch'] * (settings['nb_elements'] / settings['nb_active'])
        settings['dx_im'] = settings['pitch'] / 3.
        settings['dz'] = settings['sound_speed'] / 2 / settings['sampling_frequency']
        settings['dz_im'] = settings['sound_speed'] / 2 / settings['sampling_frequency']
        settings['z_min'] = 5e-3
        settings['z_max'] = 50e-3
        # Crop data: REQUIRED TO FEED EVEN DIMENSIONS
        Nz_min = int(2 * np.ceil(0.5 * settings['z_min'] / settings['dz_im']))  # ceil to nearest even
        Nz_max = int(2 * np.floor(0.5 * settings['z_max'] / settings['dz_im']))  # floor to nearest even
        seq.crop_data(first_index=Nz_min, last_index=Nz_max)
        x_lim, z_lim = seq.image_limits
        """
        TODO: see why it doesn't work when re-assigning computed z_lim which is exact and extremely close to 
        settings['z_max'] or settings['z_min'].
        It seems that it is somehow "out of grid" and kills the process.
        For now let's stick to the predefined values
        """

        #   Aditional required fields
        settings['distribution'] = 'uniform'

        # Measurement model
        mm = tmp_solver.measurement_model
        if mm.interpolation == 'cubic':
            settings['interpolation'] = 'cubic_spline'
        elif mm.interpolation == 'linear':
            settings['interpolation'] = 'linear'
        elif mm.interpolation == 'nearest':
            settings['interpolation'] = 'nearest_neighbour'
        else:
            raise NotImplementedError('Unsupported interpolation method {name}'.format(name=mm.interpolation))

        settings['obliquity'] = int(mm.obliquity)  # convert bool to int
        settings['propagation'] = int(mm.propagation)
        settings['pulse_convol'] = int(mm.pulse)
        if mm.pulse:
            pulse_str = ' '.join(['{}'.format(p) for p in seq.estimate_received_pulse()])
            settings['pulse'] = pulse_str

        # Assign settings to private property
        self.__settings = settings

        # Data file names
        self.__data_file_names = angles_str_list
        self.__data_list = seq.data

    # Properties
    @property
    def settings(self):
        return self.__settings

    @property
    def input_folder(self):
        return os.path.join(self.__tmp_folder, 'input')

    @property
    def output_folder(self):
        return os.path.join(self.__tmp_folder, 'output')

    @property
    def use_gpu(self):
        return self.__use_gpu

    @property
    def bin_path(self):
        if self.use_gpu:
            return self.__gpu_bin_path
        else:
            return self.__cpu_bin_path

    # Methods
    def dump_settings(self):
        filename = 'input_file.csv'
        with open(os.path.join(self.input_folder, filename), 'w') as input_file:
            for key, value in self.settings.items():
                input_file.write('{},{}\n'.format(key, value))

    def dump_data(self):
        for data, wave in zip(self.__data_list, self.__data_file_names):
            filename = 'rawdata_T_{}.csv'.format(wave)
            with open(os.path.join(self.input_folder, filename), 'wb+') as rawdata_input:
                # No need to transpose, already shape=(transducer_number, sample_number)
                np.savetxt(rawdata_input, data, delimiter=',')

    def create_tmp_folder(self):
        if not os.path.exists(self.input_folder):
            os.makedirs(self.input_folder)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def remove_tmp_folder(self):
        if os.path.exists(self.__tmp_folder):
            shutil.rmtree(self.__tmp_folder)

    def launch(self, processing_unit='CPU', run_number=1):
        # NVIDIA device and driver check
        if processing_unit == 'GPU':
            ussr.utils.ui.check_nvidia_device()

        # Inputs
        if processing_unit == 'CPU':
            self.__use_gpu = False
            self.__settings['processing_unit'] = 'CPU'
        else:
            self.__use_gpu = True
            self.__settings['processing_unit'] = 'GPU'

        self.__settings['nb_runs'] = run_number

        # Clean tmp folder
        self.remove_tmp_folder()
        self.create_tmp_folder()

        # Dump settings and data
        self.dump_settings()
        self.dump_data()

        # Launch executable
        print('\nC++ launch --------------------------------------------------')
        subprocess.call([self.bin_path, self.input_folder])

        # Read output
        output_file_name = os.path.join(self.output_folder, "rfimage_output.csv")

        output_cpp = np.genfromtxt(output_file_name,  # file name
                                   skip_header=0,  # lines to skip at the top
                                   skip_footer=0,  # lines to skip at the bottom
                                   delimiter=',',  # column delimiter
                                   dtype='float64')  # data type

        # Remove .tmp file
        self.remove_tmp_folder()

        return output_cpp
