# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os
import sys
import base64
import Config
import Functions


CONFIG = Config.Config()

MACOS_IDENTITY = CONFIG['ci']['codesign']['macos']
MACOS_CERTIFICATE_PASSWORD = sys.argv[1]
MACOS_CERTIFICATE_ENCODED = sys.argv[2]

def signLinux():
    Functions.printNeutralMessage('No code signing needed for linux')
    return

def signWindows():
    Functions.printNeutralMessage('Code signing on Windows is not supported yet')
    return

def signMacos():
    try:
        message = f'sign code on {CONFIG.os}'
        keychain_name = 'codesign.keychain'
        keychain_password = 'password'
        mac_certificate_fpath = 'certificate.p12'

        try:
            sub_message = f'create certificate file'
            certificate_decoded = base64.b64decode(MACOS_CERTIFICATE_ENCODED)
            with open(mac_certificate_fpath, 'wb') as f:
                f.write(certificate_decoded)
        except Exception as sub_exception:
            Functions.printFailMessage(sub_message, sub_exception)
            sys.exit(1)
        else:
            Functions.printSuccessMessage(sub_message)

        exit()

        try:
            sub_message = f'create keychain'
            Functions.run(
                'security', 'create-keychain',
                '-p', keychain_password,
                keychain_name)
        except Exception as sub_exception:
            Functions.printFailMessage(sub_message, sub_exception)
            sys.exit(1)
        else:
            Functions.printSuccessMessage(sub_message)

        try:
            sub_message = f'set created keychain to be default keychain'
            Functions.run(
                'security', 'default-keychain',
                '-s', keychain_name)
        except Exception as sub_exception:
            Functions.printFailMessage(sub_message, sub_exception)
            sys.exit(1)
        else:
            Functions.printSuccessMessage(sub_message)

        try:
            sub_message = f'list keychains'
            Functions.run(
                'security', 'list-keychains')
        except Exception as sub_exception:
            Functions.printFailMessage(sub_message, sub_exception)
            sys.exit(1)
        else:
            Functions.printSuccessMessage(sub_message)

        try:
            sub_message = f'unlock created keychain'
            Functions.run(
                'security', 'unlock-keychain',
                '-p', keychain_password,
                keychain_name)
        except Exception as sub_exception:
            Functions.printFailMessage(sub_message, sub_exception)
            sys.exit(1)
        else:
            Functions.printSuccessMessage(sub_message)

        try:
            sub_message = f'import certificate to created keychain'
            Functions.run(
                'security', 'import',
                mac_certificate_fpath,
                '-k', keychain_name,
                '-P', MACOS_CERTIFICATE_PASSWORD,
                '-T', '/usr/bin/codesign')
        except Exception as sub_exception:
            Functions.printFailMessage(sub_message, sub_exception)
            sys.exit(1)
        else:
            Functions.printSuccessMessage(sub_message)

        try:
            sub_message = f'show certificates'
            Functions.run(
                'security', 'find-identity',
                '-v')
        except Exception as sub_exception:
            Functions.printFailMessage(sub_message, sub_exception)
            sys.exit(1)
        else:
            Functions.printSuccessMessage(sub_message)

        try:
            sub_message = f'allow codesign to access certificate key from keychain'
            Functions.run(
                'security', 'set-key-partition-list',
                '-S', 'apple-tool:,apple:,codesign:',
                '-s',
                '-k', keychain_password, keychain_name)
        except Exception as sub_exception:
            Functions.printFailMessage(sub_message, sub_exception)
            sys.exit(1)
        else:
            Functions.printSuccessMessage(sub_message)

        try:
            sub_message = f'sign code with imported certificate'
            Functions.run(
                'codesign',
                '--deep',                   # nested code content such as helpers, frameworks, and plug-ins, should be recursively signed
                '--force',                  # replace any existing signature on the path(s) given
                '--verbose=4',              # set (with a numeric value) or increments the verbosity level of output
                '--timestamp',              # request that a default Apple timestamp authority server be contacted to authenticate the time of signin
                '--options=runtime',        # specify a set of option flags to be embedded in the code signature
                '--sign', MACOS_IDENTITY,   # sign the code at the path(s) given using this identity
                CONFIG.setup_exe_path)
        except Exception as sub_exception:
            Functions.printFailMessage(sub_message, sub_exception)
            sys.exit(1)
        else:
            Functions.printSuccessMessage(sub_message)

    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


if __name__ == "__main__":
    if CONFIG.os == 'ubuntu':
        signLinux()
    elif CONFIG.os == 'windows':
        signWindows()
    elif CONFIG.os == 'macos':
        signMacos()
    else:
        raise AttributeError(f"OS '{CONFIG.os}' is not supported")
