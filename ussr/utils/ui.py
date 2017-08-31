import os
import urllib.request
import subprocess
from urllib.parse import urlparse, urlsplit

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
        smi = subprocess.Popen(["nvidia-smi"], stdout=subprocess.PIPE)
        # output = smi.communicate()[0]  # TODO regex on this to extract list of devices and driver version
        return True
    except OSError:
        return False


def check_nvcc():
    try:
        nvcc = subprocess.Popen(["nvcc","--version"], stdout=subprocess.PIPE)
        # output = nvcc.communicate()[0]  # TODO regex on this to extract version of nvcc
        return True
    except OSError:
        return False
