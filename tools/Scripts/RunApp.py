__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os, sys
import Functions, Config


CONFIG = Config.Config()

def installationDir():
    var = CONFIG['ci']['app']['setup']['installation_dir'][CONFIG.os]
    return Functions.environmentVariable(var, var)

def appExePath():
    app_file_ext = CONFIG['ci']['app']['setup']['file_ext'][CONFIG.os]
    d = {
        'macos': os.path.join(installationDir(), CONFIG.app_name, CONFIG.app_full_name, 'Contents', 'MacOS', CONFIG.app_name),
        'ubuntu': os.path.join(installationDir(), CONFIG.app_name, CONFIG.app_name, CONFIG.app_full_name),
        'windows': os.path.join(installationDir(), CONFIG.app_name, CONFIG.app_name, CONFIG.app_full_name)
    }
    return d[CONFIG.os]

def runApp():
    Functions.printNeutralMessage(f'Installed application exe path: {appExePath()}')
    try:
        message = f'run {CONFIG.app_name}'
        if len(sys.argv) == 1:
            Functions.run(appExePath())
        else:
            if 'test' in sys.argv[1:]:
                Functions.createDir(CONFIG['ci']['project']['subdirs']['screenshots'])
            Functions.run(appExePath(), *sys.argv[1:])
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit()
    else:
        Functions.printSuccessMessage(message)

if __name__ == "__main__":
    runApp()
