"""General Helpers
"""
from zipfile import *
from pathlib import Path
import os, stat, subprocess 
import ui, shlex, sys, zlib

def rmdir(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWRITE)
            os.remove(filename)
        for name in dirs:
            os.chmod(os.path.join(root, name), stat.S_IWUSR)
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)

def mkzip(src, dest, method='default', command=None, algorithm='DEFLATED', level=9):
    if isinstance(src, Path):
        src = src.resolve().as_posix()
    if isinstance(dest, Path):
        dest = dest.resolve().as_posix()

    if os.path.isdir(src):
        os.path.join(src, '/')

    if os.path.exists(dest) and os.path.isfile(dest):
        os.unlink(dest)

    if method == "command" and command is not None:
        command = shlex.split(command.format(dest=dest, src=src), posix='win' not in sys.platform)        
        print(command)
        print(' '.join(command))
        subprocess.call(command)
    else:
        zlib.Z_DEFAULT_COMPRESSION = level
        algorithm = getattr(sys.modules[__name__], 'ZIP_' + algorithm.upper(), ZIP_DEFLATED)

        with ZipFile(dest, 'w', compression=ZIP_DEFLATED, compresslevel=level) as zf:
            for root, dirs, files in os.walk(src):
                for i, file in enumerate(files):
                    path = os.path.join(root, file)
                    zf.write(path, str(path)[len(str(src)):])

def unzip(src, dest):
    with ZipFile(src, 'r') as zf:
        zf.extractall(dest)