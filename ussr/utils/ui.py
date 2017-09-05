import os
import urllib.request
from urllib.parse import urlparse, urlsplit
import pynvml

from tqdm import tqdm


def copyfileobj_with_progress(fsrc, fdst, total=None, length=16*1024):
    """
    Copy data from file-like object fsrc to file-like object fdst.
    Same as `shutil.copyfileobj` with progress bar: https://hg.python.org/cpython/file/eb09f737120b/Lib/shutil.py#l64 
    :param fsrc: file-like object
    :param fdst: file-like object
    :param total: int
    :param length: int
    :return:
    """
    bar_format = '    {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} {rate_fmt}'
    with tqdm(total=total, unit='B', unit_scale=True, bar_format=bar_format, ncols=60) as pbar:
        while True:
            buf = fsrc.read(length)
            if not buf:
                break
            fdst.write(buf)
            pbar.update(len(buf))


def download_file(url, fdst):
    """
    Download data from `url` to file-like object fdst.
    :param url: str
    :param fdst: file-like object
    :return:
    """
    split = urlsplit(url)
    filename = os.path.basename(split.path)

    print('Downloading {}'.format(filename))

    with urllib.request.urlopen(url) as response:
        length = response.getheader('content-length')
        if length:
            total = int(length)
            copyfileobj_with_progress(response, fdst, total=total)


def check_nvidia_device():
    try:
        pynvml.nvmlInit()
        driver_version = float(pynvml.nvmlSystemGetDriverVersion())
        pynvml.nvmlShutdown()
        if driver_version < 367.48:
            raise OSError('NVIDIA driver v.{} is not supported. The driver version must be 367.48 or newer'.format(driver_version))
    except pynvml.NVMLError:
        raise OSError('NVIDIA device not found')
