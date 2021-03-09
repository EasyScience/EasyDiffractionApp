__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os
import ffmpeg
import Functions, Config


CONFIG = Config.Config()

def inputPattern():
    screenshots_dir = CONFIG['ci']['project']['subdirs']['screenshots']
    return f'{screenshots_dir}/*.png'

def outputPath():
    tutorials_dir = CONFIG['ci']['project']['subdirs']['tutorials']
    return os.path.join(tutorials_dir, 'tutorial.mp4')

def outputOptions():
    # https://trac.ffmpeg.org/wiki/Encode/H.264
    # https://slhck.info/video/2017/02/24/crf-guide.html
    # https://kkroening.github.io/ffmpeg-python/
    # https://github.com/kkroening/ffmpeg-python/issues/95
    return {
        'crf': CONFIG['ci']['app']['tutorials']['video']['crf'],
        'preset': CONFIG['ci']['app']['tutorials']['video']['preset'],
        'movflags': CONFIG['ci']['app']['tutorials']['video']['movflags'],
        'pix_fmt': CONFIG['ci']['app']['tutorials']['video']['pix_fmt']
    }

def fps():
    return CONFIG['ci']['app']['tutorials']['video']['fps']

def writeVideo():
    (
        ffmpeg
        .input(inputPattern(), pattern_type='glob', framerate=fps())
        .filter('scale', size='1280x768')
        .output(outputPath(), **outputOptions())
        .run(overwrite_output=True)
    )

def ffmpegZippedFileName():
    version = CONFIG['ci']['ffmpeg']['macos']['version']
    file_name_base = CONFIG['ci']['ffmpeg']['macos']['file_name_base']
    file_ext = CONFIG['ci']['ffmpeg']['macos']['file_ext']
    return f'{file_name_base}{version}{file_ext}'

def ffmpegUnzippedFilePath():
    exe = CONFIG['ci']['ffmpeg']['macos']['exe']
    return os.path.join(CONFIG.download_dir, exe)

def ffmpegDownloadUrl():
    base_url = CONFIG['ci']['ffmpeg']['macos']['base_url']
    return f'{base_url}/{ffmpegZippedFileName()}'

def ffmpegDownloadDest():
    return os.path.join(CONFIG.download_dir, f'{ffmpegZippedFileName()}')

def downloadFfmpeg():
    Functions.downloadFile(
        url=ffmpegDownloadUrl(),
        destination=ffmpegDownloadDest()
    )

def unzipFfmpeg():
    if os.path.exists(ffmpegUnzippedFilePath()):
        Functions.printNeutralMessage(f'File already exists {ffmpegUnzippedFilePath()}')
        return
    Functions.unzip(ffmpegDownloadDest(), CONFIG.download_dir)
    Functions.addReadPermission(ffmpegUnzippedFilePath())

def addDownloadDestToPath():
    path = Functions.environmentVariable('PATH')
    download_dest = os.path.abspath(CONFIG.download_dir)
    Functions.setEnvironmentVariable('PATH', f'{download_dest}:{path}')

if __name__ == "__main__":
    #downloadFfmpeg()
    #unzipFfmpeg()
    #addDownloadDestToPath()
    #writeVideo()
    Functions.copyFile('tutorial.mp4', outputPath())
