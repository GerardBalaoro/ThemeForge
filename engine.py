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
            'compress': [
                'com.android.*',
                'com.bbm.*',
                'com.vivo.*',
                'com.huawei.*',
                'framework-*',
                'com.bbk.*',
            ],
            'ignore': [
                '.*'
            ]
        }
    }
    
    def __init__(self, path):
        path = Path(path)
        if not path.exists():
            if path.is_dir():
                os.mkdir(path)
            else:
                raise FileNotFoundError('The file {} cannot be found.'.format(path))

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
        json.dump(self.config, file, indent=True)
        file.close()
    
    def build(self, dest):
        self.load()
        ui.block(self.sourceDirectory, 'Build Finished', padding=5)

        contents = os.listdir(self.sourceDirectory)
        digits = len(str(len(contents)))

        if os.path.isdir(self.buildDirectory):
            ui.line('[{}] Cleaning Build Folder'.format('.' * (digits * 2 + 1)), pre=' - ')
            tools.rmdir(self.buildDirectory)
        os.mkdir(self.buildDirectory)

        for i, path in enumerate(contents):
            if [fnmatch.fnmatch(path, pat) for pat in self.config['engine']['ignore']].count(True) == 0:
                realpath = self.sourceDirectory.joinpath(path)
                ui.line('[{}/{}]'.format(str(i + 1).zfill(digits), len(contents)), end=' ', pre=' - ')

                if os.path.isdir(realpath):
                    if [fnmatch.fnmatch(path, pat) for pat in self.config['engine']['compress']].count(True):
                        ui.line('Archiving Folder: {}'.format(path))
                        tools.mkzip(realpath, self.buildDirectory.joinpath(path))
                    else:
                        ui.line('Copying Folder: {}'.format(path))
                        shutil.copytree(realpath, self.buildDirectory.joinpath(path))
                elif os.path.isfile(realpath):
                    ui.line('Copying File: {}'.format(path))
                    shutil.copy(realpath, self.buildDirectory)

        ui.line('[{}] Compiling Theme Package'.format('.' * (digits * 2 + 1)), pre=' - ')
        tools.mkzip(self.buildDirectory, dest)
        ui.block(dest, 'Build Finished', padding=5)

    def unpack(self, file):
        self.load()
        ui.block(file, 'Unpacking Theme', padding=5)

        ui.line('Unpacking Theme Package', pre=' - ')
        if self.cacheDirectory.exists():
            tools.rmdir(self.cacheDirectory)
        tools.unzip(file, self.cacheDirectory)

        contents = os.listdir(self.cacheDirectory)
        for i, path in enumerate(contents):
            realpath = self.cacheDirectory.joinpath(path)

            if os.path.isfile(realpath) and [fnmatch.fnmatch(path, pat) for pat in self.config['engine']['compress']].count(True):
                ui.line('Unpacking Asset: {}'.format(path), pre=' - ')
                scrap = realpath.with_suffix('.scrap')
                os.rename(realpath, scrap)
                try:
                	tools.unzip(scrap, self.cacheDirectory.joinpath(path))
                	os.unlink(scrap)
                except:
                	if os.path.exists(realpath):
                		tools.rmdir(realpath)
                	ui.line('Failed to Unpack: {}'.format(path), pre=' - ')
                	os.rename(scrap, realpath)

        ui.line('Moving to Working Directory'.format(path), pre=' - ')
        if self.sourceDirectory.exists():
            tools.rmdir(self.sourceDirectory)
        self.cacheDirectory.rename(self.sourceDirectory)

        ui.block(self.sourceDirectory, 'Unpacking Finished')