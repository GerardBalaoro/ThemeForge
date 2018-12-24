"""General Helpers
"""
from zipfile import ZipFile
import os, stat

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

def mkzip(src, dest):
    if os.path.exists(dest) and os.path.isfile(dest):
        os.unlink(dest)

    with ZipFile(dest, 'w') as zf:
        for root, dirs, files in os.walk(src):
            for i, file in enumerate(files):
                path = os.path.join(root, file)
                zf.write(path, str(path)[len(str(src)):])

def unzip(src, dest):
    with ZipFile(src, 'r') as zf:
        zf.extractall(dest)