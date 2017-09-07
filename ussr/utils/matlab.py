from scipy.io import savemat
import ussr.sequence
import numpy as np
import os


def export(dir_name, rf_image, sequence):
    tmp_seq = sequence
    if not isinstance(rf_image, np.ndarray):
        raise TypeError

    if not isinstance(tmp_seq, ussr.sequence.PWSequence):
        raise TypeError

    xlim, zlim = tmp_seq.image_limits
    mdict = dict()
    Nzim = rf_image.shape[1]
    Nxim = rf_image.shape[0]
    mdict['zim'] = np.linspace(zlim[0], zlim[1], Nzim)
    mdict['xim'] = np.linspace(xlim[0], xlim[1], Nxim)
    mdict['rf_data'] = rf_image.T
    mdict['number_plane_waves'] = len(tmp_seq.angles)
    if 'carotid' in tmp_seq.name:
        filename_seq = (tmp_seq.name, 'nbPW', str(len(tmp_seq.angles)))
        filename = '_'.join(filename_seq)
    else:
        filename = tmp_seq.name
    path = os.path.join(dir_name, filename)
    savemat(file_name=path, mdict=mdict, appendmat=True)




