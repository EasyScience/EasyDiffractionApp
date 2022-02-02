# SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os, sys
import Functions, Config


CONFIG = Config.Config()

def source():
    return CONFIG.setup_exe_path

def destination():
    file_suffix = Functions.artifactsFileSuffix(sys.argv[1])
    setup_zip_name = f'{CONFIG.setup_name}{file_suffix}.zip'
    setup_zip_path = os.path.join(CONFIG.dist_dir, setup_zip_name)
    return setup_zip_path

def zip():
    Functions.zip(source(), destination())

if __name__ == "__main__":
    zip()
