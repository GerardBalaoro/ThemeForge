import json, os, fnmatch
import shutil, ui, tools
from pathlib import Path

class Theme:
    root = ''
    config = {
        'workspace': {
            'build': 'build',
            'source': 'theme',
            'cache': '.cache',
        },
        'engine': {
            'zip': [
                'com.android.*',
                'com.bbm.*',
                'com.vivo.*',
                'com.huawei.*',
                'framework-*',
                'com.bbk.*',
            ],
            'ignore': [
                '.*'
            ],
            'compression': {
                'method': 'default',
                'command': '7z a -tzip -m0=lzma -mx=9 {dest} {src}',
                'algorithm': 'DEFLATED',
                'level': 9
            }            
        }
    }
    
    def __init__(self, path):
        path = Path(path)
        if not path.exists():
            os.mkdir(path)

        if path.is_file():
            self.root = path.parent.resolve()
        elif path.is_dir():
            self.root = path.resolve()
        self.load()
        self.save()
        ui.title()

    @property
    def sourceDirectory(self):
        path = Path(self.config['workspace']['source'])
        if path.is_absolute():
            return path
        else:
            return Path(self.root).joinpath(path)


    @property
    def buildDirectory(self):
        path = Path(self.config['workspace']['build'])
        if path.is_absolute():
            return path
        else:
            return Path(self.root).joinpath(path)

    @property
    def cacheDirectory(self):
        path = Path(self.config['workspace']['cache'])
        if path.is_absolute():
            return path
        else:
            return Path(self.root).joinpath(path)

    @property
    def configPath(self):
        return Path(self.root).joinpath('forge.json')

    def load(self):
        if self.configPath.exists() and self.configPath.is_file():
            file = open(self.configPath, 'r')
            self.config = json.load(file)
            file.close()

    def save(self):
        file = open(self.configPath, 'w+')
        json.dump(self.config, file, indent='\t')
        file.close()
    
    def build(self, dest):
        self.load()
        ui.block(self.sourceDirectory, 'Build Started', padding=5)

        contents = os.listdir(self.sourceDirectory)
        compression = self.config['engine']['compression']

        if os.path.isdir(self.buildDirectory):
            ui.line('Cleaning Build Folder')
            tools.rmdir(self.buildDirectory)
        os.mkdir(self.buildDirectory)

        def mkzip(src, dest):
            tools.mkzip(src, dest, compression['method'], compression['command'], compression['algorithm'], int(compression['level']))

        for i, path in enumerate(contents):
            if [fnmatch.fnmatch(path, pat) for pat in self.config['engine']['ignore']].count(True) == 0:
                realpath = self.sourceDirectory.joinpath(path)

                try:                    
                    if os.path.isdir(realpath):
                        if [fnmatch.fnmatch(path, pat) for pat in self.config['engine']['zip']].count(True):
                            ui.line('Archiving Folder: {}'.format(path))
                            mkzip(realpath, self.buildDirectory.joinpath(path))
                        else:
                            ui.line('Copying Folder: {}'.format(path))
                            shutil.copytree(realpath, self.buildDirectory.joinpath(path))
                    elif os.path.isfile(realpath):
                        ui.line('Copying File: {}'.format(path))
                        shutil.copy(realpath, self.buildDirectory)
                except Exception as e:
                    ui.line('Action Failed: {}'.format(e))

        ui.line('Compiling Theme Package'.format())
        mkzip(self.buildDirectory, dest)
        ui.block(dest, 'Build Finished', padding=5)

    def unpack(self, file):
        self.load()
        ui.block(file, 'Unpacking Theme', padding=5)

        ui.line('Unpacking Theme Package')
        if self.cacheDirectory.exists():
            tools.rmdir(self.cacheDirectory)
        tools.unzip(file, self.cacheDirectory)

        contents = os.listdir(self.cacheDirectory)
        for i, path in enumerate(contents):
            realpath = self.cacheDirectory.joinpath(path)

            if os.path.isfile(realpath) and [fnmatch.fnmatch(path, pat) for pat in self.config['engine']['zip']].count(True):
                ui.line('Unpacking Asset: {}'.format(path))
                scrap = realpath.with_suffix('.scrap')
                os.rename(realpath, scrap)
                try:
                	tools.unzip(scrap, self.cacheDirectory.joinpath(path))
                	os.unlink(scrap)
                except:
                	if os.path.exists(realpath):
                		tools.rmdir(realpath)
                	ui.line('Failed to Unpack: {}'.format(path))
                	os.rename(scrap, realpath)

        ui.line('Moving to Working Directory'.format(path))
        if self.sourceDirectory.exists():
            tools.rmdir(self.sourceDirectory)
        self.cacheDirectory.rename(self.sourceDirectory)

        ui.block(self.sourceDirectory, 'Unpacking Finished')