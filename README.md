# USSR: An UltraSound Sparse Regularization framework
[Ecole Polytechnique Fédérale de Lausanne (EPFL)]: http://www.epfl.ch/
[Signal Processing Laboratory (LTS5)]: http://lts5www.epfl.ch
[IEEE International Ultrasonics Symposium (IUS 2017)]: http://ewh.ieee.org/conf/ius/2017/
[Institute of Sensors, Signals and Systems]: https://www.hw.ac.uk/schools/engineering-physical-sciences/institutes/sensors-signals-systems/basp.htm
[Heriot-Watt University]:https://www.hw.ac.uk/
[paper]:https://infoscience.epfl.ch/record/229453/files/IUS2017_USSR_An_UltraSound_Sparse_Regularization_Framework.pdf
[PICMUS submodule]:https://bitbucket.org/picmus/picmus

Adrien Besson<sup>1</sup>, Dimitris Perdios<sup>1</sup>, Florian Martinez<sup>1</sup>, Marcel Arditi<sup>1</sup>, Yves Wiaux<sup>2</sup> and Jean-Philippe Thiran<sup>1, 3</sup>

<sup>1</sup>[Signal Processing Laboratory (LTS5)], [Ecole Polytechnique Fédérale de Lausanne (EPFL)], Switzerland

<sup>2</sup>[Institute of Sensors, Signals and Systems], [Heriot-Watt University] , UK

<sup>3</sup>Department of Radiology, University Hospital Center (CHUV), Switzerland

Code used to reproduce the results presented in this [paper], accepted at the IEEE International Ultrasonics Symposium 2017

## Requirements
  * Linux (code tested on Linux Mint 18.1)
  * Python >= 3.5
  * pip (with setuptools and wheel)
  * MATLAB (code tested on MATLAB R2016b and R2017a)
  * git
  * (Optional) NVIDIA GPU with Kepler or newer architecture and NVIDIA CUDA

## Installation
1. (Optional) Create a dedicated Python environment
1. Clone the repository (``--recursive`` is used to download the [PICMUS submodule] when cloning the repo)
    ```bash
    git clone --recursive https://github.com/LTS5/USSR-IUS2017.git
    ```
1. Enter in the `USSR-IUS2017` folder
    ```bash
    cd USSR-IUS2017
    ```
1. Install the Python dependencies from `python_requirements.txt`
    ```bash
    pip install --upgrade pip
    pip install --upgrade -r python_requirements.txt
    ```

## Reproduce the results of the paper
1. Launch the bash file
    * To run the GPU version of the code
        ```bash
        ./ius_results.sh 'GPU'
        ```
    * To run the CPU version of the code
        ```bash
        ./ius_results.sh 'CPU'
        ```
    The bash file does the following operations:
     * Download the PICMUS datasets (may take some time depending on your Internet connection)
     * Reconstruct the images
     * Compute and export the metrics
     * Generate and export the figures

1. The folder `USSR-IUS2017/results` contains the metrics reported in Table I of the [paper] and the B-mode images displayed on Figure 2 of the [paper]

## Remarks
The code uses NVIDIA CUDA and therefore is only compatible with NVIDIA GPUs. It should support every GPU architecture starting from Kepler (compute capability >= 3.0).
The code has been tested on the following architectures:
 * NVIDIA Titan X GPU (cc = 6.1) and NVIDIA GeForce GT 630 (cc = 3.5)
 * Intel(R) Core(TM) i7-4930K CPU @ 3.40GHz

The CPU version of the code may take a very long time. It took 10 minutes to run 200 iterations of FISTA on the above mentioned CPU.

## Developers
 * Florian Martinez (florian.martinez@epfl.ch): CUDA and C/C++
 * Dimitris Perdios (dimitris.perdios@epfl.ch): Python interface
 * Adrien Besson (adrien.besson@epfl.ch): Matlab interface

## License
[License](LICENSE.txt) for non-commercial use of the software. Please cite the following [paper] when using the code.
