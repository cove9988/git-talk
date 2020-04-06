
import os
import configparser
import shutil
class conf():
    def __init__(self, ini_file):
        f = os.path.abspath('./git_talk/' + ini_file)
        con_file = os.path.join(os.path.expanduser('~'), ini_file)
        if not os.path.exists(con_file):
            print('copy file to: ', con_file, ' from: ', f)
            shutil.copyfile(f, con_file)
        self.ini_file = con_file
        self.cfg = configparser.ConfigParser()
        self.cfg.read(self.ini_file)

    def save(self, section,option,value):
        self.cfg.set(section,option,value)
        with open(self.ini_file,'w') as c:
            self.cfg.write(c) 
    
    def value(self,section,option):
        return self.cfg[section][option]

    def values(self,section):
        return [{x:y} for x, y in self.cfg[section].items() ]

    def options(self, section):
        return self.cfg[section]