'''
create VERSION.json if not exist with 0.0.0
get version
set version
'''
import os
import json
class VersionController():
    def __init__(self, version_path):
        self.path_file = os.path(version_path,'version.json')
        
    def version(self, ver=''):
        with open(self.path_file, 'rw') as f:
            d = json.load(f)
            if d is None:
                d = {"version":"0.0.0"}
            if ver:
                return d['version']
            else:
                d['version'] = ver
                json.jump(d, f)
                return ''
