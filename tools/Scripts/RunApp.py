__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os, sys
import pathlib
import Functions, Config


CONFIG = Config.Config()

def installationDir():
    if CONFIG.installation_dir_shortcut == '@HomeDir@':
        return str(pathlib.Path.home())
    elif CONFIG.installation_dir_shortcut == '@ApplicationsDirX86@' and CONFIG.os == 'windows':
        return Functions.environmentVariable('ProgramFiles(x86)')
    elif CONFIG.installation_dir_shortcut == '@ApplicationsDir@' and CONFIG.os == 'windows':
        return Functions.environmentVariable('ProgramFiles')
    elif CONFIG.installation_dir_shortcut == '@ApplicationsDir@' and CONFIG.os == 'ubuntu':
        return '/opt'
    elif CONFIG.installation_dir_shortcut == '@ApplicationsDir@' and CONFIG.os == 'macos':
        return '/Applications'
    elif CONFIG.installation_dir_shortcut == '@ApplicationsDirUser@' and CONFIG.os == 'macos':
        return str(pathlib.Path.home().joinpath('Applications'))
    return var  # Functions.environmentVariable(var, var)

def appExePath():
    prefix = os.path.join(installationDir(), CONFIG.app_name)
    d = {
        'macos': os.path.join(prefix, CONFIG.app_full_name, 'Contents', 'MacOS', CONFIG.app_name),
        'ubuntu': os.path.join(prefix, CONFIG.app_name, CONFIG.app_full_name),
        'windows': os.path.join(prefix, CONFIG.app_name, CONFIG.app_full_name)
    }
    return d[CONFIG.os]

def runApp():
    Functions.printNeutralMessage(f'Installed application exe path: {appExePath()}')
    try:
        message = f'run {CONFIG.app_name}'
        if len(sys.argv) == 1:
            Functions.run(appExePath())
        else:
            #if 'test' in sys.argv[1:]:
            #    Functions.createDir(CONFIG.screenshots_dir)
            Functions.run(appExePath(), *sys.argv[1:])
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit()
    else:
        Functions.printSuccessMessage(message)

if __name__ == "__main__":
    runApp()
