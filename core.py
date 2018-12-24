import json, os, fnmatch
import shutil, ui, tools
from pathlib import Path

class Theme:

    root = ''
    config = {
        'workspace': {
            'build': 'build',
            'working': 'theme',
            'temp': '.temp',
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
        if path.exists():
            if path.is_file():
                self.root = path.parent.resolve()
            elif path.is_dir():
                self.root = path.resolve()
            self.load()
        self.save()
        ui.title()

    @property
    def workingDirectory(self):
        path = Path(self.config['workspace']['working'])
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
    def tempDirectory(self):
        path = Path(self.config['workspace']['temp'])
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
        ui.table ([['- Build  Finished -'], [self.workingDirectory]], padding=5)

        contents = os.listdir(self.workingDirectory)
        digits = len(str(len(contents)))

        if os.path.isdir(self.buildDirectory):
            ui.line('[{}] Cleaning Build Folder'.format('.' * (digits * 2 + 1)), type='info', pre=' - ')
            tools.rmdir(self.buildDirectory)
        os.mkdir(self.buildDirectory)        

        for i, path in enumerate(contents):
            if [fnmatch.fnmatch(path, pat) for pat in self.config['engine']['ignore']].count(True) == 0:
                realpath = self.workingDirectory.joinpath(path)
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

        ui.line('[{}] Compiling Theme Package'.format('.' * (digits * 2 + 1)), type='info', pre=' - ')
        tools.mkzip(self.buildDirectory, dest)
        ui.table ([[ui.text['success']('- Build  Finished -')], [dest]], padding=5)

    def unpack(self, file):
        self.load()
        ui.table([['-- Unpacking Theme --'], [file]], padding=5)

        ui.line('Unpacking Theme Package', type='info', pre=' - ')
        if self.tempDirectory.exists():
            tools.rmdir(self.tempDirectory)
        tools.unzip(file, self.tempDirectory)

        contents = os.listdir(self.tempDirectory)
        for i, path in enumerate(contents):
            realpath = self.tempDirectory.joinpath(path)

            if os.path.isfile(realpath) and [fnmatch.fnmatch(path, pat) for pat in self.config['engine']['compress']].count(True):
                ui.line('Unpacking Asset: {}'.format(path), pre=' - ')
                scrap = realpath.with_suffix('.scrap')
                os.rename(realpath, scrap)
                tools.unzip(scrap, self.tempDirectory.joinpath(path))
                os.unlink(scrap)

        ui.line('Moving to Working Directory'.format(path), type='warn', pre=' - ')
        if self.workingDirectory.exists():
            tools.rmdir(self.workingDirectory)
        self.tempDirectory.rename(self.workingDirectory)

        ui.table([[ui.text['success']('- Unpacking Finished -')], [self.workingDirectory]], padding=3)
                