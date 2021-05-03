<img src="https://easydiffraction.github.io/images/easydiffraction-logo.svg" height="80"><img width="15"><img src="https://easydiffraction.github.io/images/easydiffraction-text.svg" height="80">

**easyDiffraction** is a scientific software for modelling and analysis of the diffraction data. Currently, **easyDiffraction** covers
classical 1D unpolarized neutron single crystal and powder diffraction data collected at a constant wavelength.

## Main features

**easyDiffraction** allows simulation of diffraction patterns based on a structural model and refinement (fitting) of its parameters.
For refinement, the program uses a number of fitting engines and minimizers.

**easyDiffraction** is similar to crystallographic programs like FullProf, Jana, GSAS, ShelX.

In contrast to these programs, **easyDiffraction** is based on _external_ crystallographic libraries,
such as CrysPy and CrysFML in order to cover different functionality aspects within a single intuitive and user-friendly graphical interface.
These libraries are included with the installation so there is no need to download and compile any additional components.

**easyDiffraction** is of course open source (currently GPLv3, migrating to BSD) and cross-platform, with support for Windows, macOS and Linux (Ubuntu).

The intuitive tabbed interface with built-in step-by-step user guides, video tutorials, as well as a clear workflow help speed up data modelling and analysis.

Current main features of **easyDiffraction**:

* support for constant-wavelength, unpolarized data
* simulations of diffraction pattern using CrysPy and CrysFML
* pattern refinement using CrysPy and CrysFML
* multiple minimizing engines: bumps, lmfit, DFO-LS
* structure viewer and builder
* pattern viewer including HKL position chart and difference chart
* interactive HTML and standard PDF report generation

Planned functionality for **easyDiffraction** includes support for:

* time-of-flight data
* polarized data
* additional libraries, e.g. GSASII
* magnetic structures
* pair-distribution-function analysis
* X-ray experiments

## Dev info

[![CI Build][20]][21]

[![Release][30]][31]

[![Downloads][70]][71] [![Lines of code][82]][80] [![Total lines][81]][80] [![Files][83]][80]

[![License][50]][51]

[![w3c][90]][91]

### Download easyDiffractionApp repo
* Open **Terminal** 
* Change the current working directory to the location where you want the **easyDiffractionApp** directory
* Clone **easyDiffractionApp** repo from GitHub using **git**
  ```
  git clone https://github.com/easyScience/easyDiffractionApp
  ```
  
### Install easyDiffractionApp dependencies
* Open **Terminal**
* Install [**Poetry**](https://python-poetry.org/docs/) (Python dependency manager)
  * osx / linux / bashonwindows
    ```
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
    ```
  * windows powershell
    ```
    (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
    ```
* Go to **easyDiffractionApp** directory
* Create virtual environment for **easyDiffractionApp** and install its dependences using **poetry** (configuration file: **pyproject.toml**)
  ```
  poetry install
  ```
  
### Launch easyDiffractionApp application
* Open **Terminal**
* Go to **easyDiffractionApp** directory
* Launch **easyDiffraction** application using **poetry**
  ```
  poetry run easyDiffraction
  ```

### Update easyDiffractionApp dependencies
* Open **Terminal**
* Go to **easyDiffractionApp** directory
* Update **easyDiffractionApp** using **poetry** (configuration file: **pyproject.toml**)
  ```
  poetry update
  ```

### Delete easyDiffractionApp
* Delete **easyDiffractionApp** directory
* Uninstall **Poetry**
   * osx / linux / bashonwindows
   ```
   curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | POETRY_UNINSTALL=1 python
   ```

<!---URLs--->
<!---https://naereen.github.io/badges/--->

<!---CI Build Status--->
[20]: https://github.com/easyScience/easyDiffractionApp/workflows/build%20macOS,%20Linux,%20Windows/badge.svg
[21]: https://github.com/easyScience/easyDiffractionApp/actions?query=workflow%3A%22build+macOS%2C+Linux%2C+Windows%22

<!---Release--->
[30]: https://img.shields.io/github/release/easyScience/easyDiffractionApp.svg
[31]: https://github.com/easyScience/easyDiffractionApp/releases

<!---License--->
[50]: https://img.shields.io/github/license/easyScience/easyDiffractionApp.svg
[51]: https://github.com/easyScience/easyDiffractionApp/blob/master/LICENSE.md

<!---LicenseScan--->
[60]: https://app.fossa.com/api/projects/git%2Bgithub.com%2FeasyScience%2FeasyDiffractionApp.svg?type=shield
[61]: https://app.fossa.com/projects/git%2Bgithub.com%2FeasyScience%2FeasyDiffractionApp?ref=badge_shield

<!---Downloads--->
[70]: https://img.shields.io/github/downloads/easyScience/easyDiffractionApp/total.svg
[71]: https://github.com/easyScience/easyDiffractionApp/releases

<!---Code statistics--->
[80]: https://github.com/easyScience/easyDiffractionApp
[81]: https://tokei.rs/b1/github/easyScience/easyDiffractionApp
[82]: https://tokei.rs/b1/github/easyScience/easyDiffractionApp?category=code
[83]: https://tokei.rs/b1/github/easyScience/easyDiffractionApp?category=files

<!---W3C validation--->
[90]: https://img.shields.io/w3c-validation/default?targetUrl=https://easyscience.github.io/easyDiffractionApp
[91]: https://easyscience.github.io/easyDiffractionApp
