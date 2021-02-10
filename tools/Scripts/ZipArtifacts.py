__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os, sys
import Functions, Config


CONFIG = Config.Config()

def zipFileSuffix():
    short_github_ref = sys.argv[1]
    if short_github_ref == '2/merge':
        return '_PR'
    if short_github_ref != 'master':
        return f'_{short_github_ref}'
    return ''

def source():
    return CONFIG.setup_exe_path

def destination():
    setup_zip_name = f'{CONFIG.setup_name}{zipFileSuffix()}.zip'
    setup_zip_path = os.path.join(CONFIG.dist_dir, setup_zip_name)
    return setup_zip_path

def zip():
    Functions.zip(source(), destination())

if __name__ == "__main__":
    zip()
