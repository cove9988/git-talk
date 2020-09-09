import os
import configparser
import shutil
import json


# cc = lib.config.conf('.git_talk.ini')

# m = cc.value('repo_json','git-talk')
# mm = json.loads(m)
# mm["jira-link"] = "test"
# mm["version"] = "1.0.1"
# mmm = json.dumps(mm)
# cc.save('repo_json','git-talk',mmm)


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
    
    def value_json(self, section,option):
        return json.loads(self.value(section,option))

    def save_json(self, section,option,value_json):
        self.save(section,option,json.dumps(value_json))
    
    def values_json(self,section):
        return [{x:json.loads(y)} for x, y in self.cfg[section].items()]
