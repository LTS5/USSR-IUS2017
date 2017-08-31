import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1


def convert_to_bmode(data, normalize=True):
    data_bm = np.abs(scipy.signal.hilbert(data, axis=1))
    if normalize:
        data_bm /= np.abs(data_bm).max()
    data_bm = 20 * np.log10(data_bm)

    return data_bm


def plot_bmode(data, db_range=40, x_lim=None, z_lim=None, axis_scale=1e3, cbar=False, ax=None, show_axes=True):

    if ax is None:
        ax = plt.gca()

    extent = None
    if x_lim is not None and z_lim is not None:
        extent = [x_lim[0], x_lim[1], z_lim[1], z_lim[0]]
        extent = [val*axis_scale for val in extent]

    im = ax.imshow(data.T, cmap='gray', vmin=-db_range, vmax=0, extent=extent, interpolation=None)

    if not show_axes:
        ax.set_axis_off()

    ax.set_xlabel('x [mm]')
    ax.set_ylabel('z [mm]')

    if cbar:
        divider = mpl_toolkits.axes_grid1.make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.1)
        plt.colorbar(im, cax=cax, label='dB [─]')
