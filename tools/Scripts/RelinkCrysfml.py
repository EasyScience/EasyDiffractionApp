__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os, sys
import importlib
import Functions, Config


CONFIG = Config.Config()

def pythonDylib():
    python_location = sys.argv[1]
    python_dylib_file = {
        'macos': 'libpython3.7m.dylib',
        'ubuntu': 'libpython3.7m.so.1.0'
    }[CONFIG.os]
    return os.path.join(python_location, 'lib', python_dylib_file)

def crysfmlPythonDylib():
    d = {
        'macos': '/Library/Frameworks/Python.framework/Versions/3.7/Python',
        'ubuntu': 'libpython3.7m.so.1.0'
    }
    return d[CONFIG.os]

def crysfmlSo():
    lib = CONFIG['ci']['pyinstaller']['libs'][CONFIG.os]
    lib_path = importlib.import_module(lib).__path__[0]
    so_location = os.path.join(lib_path, 'CFML')
    so_file = {
        'macos': 'powder_generation.so',
        'ubuntu': 'powder_generation.so'
    }[CONFIG.os]
    return os.path.join(so_location, so_file)

def relinkCrysfml():
    if CONFIG.os == 'windows':
        Functions.printNeutralMessage(f'No CrysFML relinking is needed for platform {CONFIG.os}')
        return
    try:
        message = f'relink CrysFML from default Python dylib for platform {CONFIG.os}'
        if CONFIG.os == 'macos':
            Functions.run('install_name_tool', '-change', crysfmlPythonDylib(), pythonDylib(), crysfmlSo())
        elif CONFIG.os == 'ubuntu':
            Functions.run('patchelf', '--replace-needed', crysfmlPythonDylib(), pythonDylib(), crysfmlSo())
        else:
            Functions.printFailMessage(f'Platform {CONFIG.os} is unsupported')
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit()
    else:
        Functions.printSuccessMessage(message)


if __name__ == "__main__":
    print("pythonDylib:", pythonDylib())
    print("crysfmlPythonDylib:", crysfmlPythonDylib())
    print("crysfmlSo:", crysfmlSo())
    relinkCrysfml()
