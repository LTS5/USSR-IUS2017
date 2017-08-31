import os

import ussr.data.picmus

PICMUS17_PATH = os.path.join('data', 'picmus17')
PICMUS16_PATH = os.path.join('data', 'picmus16')
pw_number_selection_list = [1, 5]
# Download PICMUS 2017 data

ussr.data.picmus.download_2017(export_path=PICMUS17_PATH, signal_selection=None, pht_selection=None, transmission_selection=None, pw_number_selection=pw_number_selection_list)
# Download PICMUS 2016 experimental data
ussr.data.picmus.download_in_vivo_2016(export_path=PICMUS16_PATH)
