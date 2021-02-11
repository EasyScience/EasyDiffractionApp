import os, sys
import ast
import zipfile
import Config
import Functions


CONFIG = Config.Config()

app_name = CONFIG.app_name
app_url = CONFIG['tool']['poetry']['homepage']
installer_exe_path = os.path.join(CONFIG.dist_dir, CONFIG.setup_full_name)

certificates_dir_path = CONFIG['ci']['project']['subdirs']['certificates_path'] # use basdir of certificate_file_path!!
certificate_file_path = CONFIG.certificate_path
certificates_zip_path = CONFIG.certificate_zip_path

certificate_password = sys.argv[1]
zip_password = sys.argv[2]

print('* Unzip certificates')
with zipfile.ZipFile(certificates_zip_path) as zf:
    zf.extractall(
        path = certificates_dir_path,
        pwd = bytes(zip_password, 'utf-8')
        )

def sign_linux():
    print('* No code signing needed for linux')
    return


def sign_windows():
    print('* Code signing for windows')

    # using local signtool, since installing the whole SDK is a total overkill
    # signtool_exe_path = os.path.join('C:', os.sep, 'Program Files (x86)', 'Windows Kits', '10', 'bin', 'x86', 'signtool.exe')
    signtool_exe_path = os.path.join(certificates_dir_path, 'signtool.exe')

    Functions.run(
        'certutil.exe',
        '-p', certificate_password,          # the password for the .pfx file
        '-importpfx', certificate_file_path  # name of the .pfx file
        )

    print('* Sign code with imported certificate')
    Functions.run(
        signtool_exe_path, 'sign',             # info - https://msdn.microsoft.com/en-us/data/ff551778(v=vs.71)
        '/f', certificate_file_path,           # signing certificate in a file
        '/p', certificate_password,            # password to use when opening a PFX file
        '/d', app_name,                        # description of the signed content
        '/du', app_url,                        # URL for the expanded description of the signed content
        '/t', 'http://timestamp.digicert.com', # URL to a timestamp server
        '/v',                                  # display the verbose version of operation and warning messages
        '/a',                                  # Select the best signing cert automatically
        installer_exe_path
        )


def sign_macos():
    keychain_name = 'codesign.keychain'
    keychain_password = 'password'
    identity = 'Developer ID Application: European Spallation Source Eric (W2AG9MPZ43)'

    print('* Create keychain')
    Functions.run(
        'security', 'create-keychain',
        '-p', keychain_password,
        keychain_name
        )

    print('* Set it to be default keychain')
    Functions.run(
        'security', 'default-keychain',
        '-s', keychain_name
        )

    print('* List keychains')
    Functions.run(
        'security', 'list-keychains'
        )

    print('* Unlock created keychain')
    Functions.run(
        'security', 'unlock-keychain',
        '-p', keychain_password,
        keychain_name
        )

    print('* Import certificate to created keychain')
    Functions.run(
        'security', 'import',
        certificate_file_path,
        '-k', keychain_name,
        '-P', certificate_password,
        '-T', '/usr/bin/codesign'
        )

    print('* Show certificates')
    Functions.run(
        'security', 'find-identity',
        '-v'
        )

    print('* Allow codesign to access certificate key from keychain')
    Functions.run(
        'security', 'set-key-partition-list',
        '-S', 'apple-tool:,apple:,codesign:',
        '-s',
        '-k', keychain_password
        )

    print('* Sign code with imported certificate')
    Functions.run(
        'codesign',
        '--deep',
        '--force',
        '--verbose',
        # --timestamp URL
        '--sign', identity,
        installer_exe_path
        )


if __name__ == "__main__":
    if CONFIG.os == 'linux':
        sign_linux()
    elif CONFIG.os == 'windows':
        sign_windows()
    elif CONFIG.os == 'osx':
        sign_macos()
    else:
        raise AttributeError("Incorrect OS")