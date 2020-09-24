import os
import csv
import time

# from git_talk import __version__
import git_talk.lib.gfunc as gfunc
import git_talk.lib.cutie as cutie
import git_talk.menu.status as stts
import git_talk.menu.branches as branches

# def save_current_project(cc, repo):
#     cc.save_json()
PROJECT_SPACE =30
VERSION_SPACE =10
PATH_SPACE = 40
display_string = "{:<" + str(PROJECT_SPACE) + "}{:<" +str(VERSION_SPACE) + "}{:<" + str(PATH_SPACE) + "}"
def project(cc):
    user_git_repo_list = [i for i in cc.values_json('repo_json')]

    names = []
    repos = []
    version = []
    repo = {}
    create_msg = cc.value('project', 'create_message')
    # TODO: max lenght for each column + 2
    for r in user_git_repo_list:
        for k, v in r.items():
            n = display_string.format(v["name"],v["version"],v["path"])
            names.append(n)
    names.append(create_msg)

    lns = cc.value('project', 'branch') + "\n"
    lns += display_string.format("    Project","    Tag", "Path")
    name = cutie.select_propmt(lns, names)
    name = name[:PROJECT_SPACE-1].strip()
    if name == create_msg:
        repo = create_project(cc)
    elif name.lower() in ('exit','cancel'):
        cutie.get_exit()
        return None
    else:
        for r in user_git_repo_list:
            for k, v in r.items():
                if name == k :
                    repo = v
                    branches.pick_branch(cc, repo)
                    cc.save_json('repo_json',repo["name"], repo )
    return repo

def create_project(cc):
    repo = {}
    # if prompt_yn(cc.value('project','create_doyou')):
    # input directory and git clone
    #pro = cutie.get_input(cc.value('project','project_name'))
    cnt = 0
    
    user,password = '',''   
    if (cutie.prompt_yn("Do you use ssh connect to repository?")):
        repo["connection-ssh"] = True
    else :
        repo["connection-ssh"] = False

    while True:
        cnt += 1
        repo['url'] = cutie.get_input(cc.value('project', 'project_url'))
        repo['name'] = stts.get_repo_name(url=repo['url'])
        # {"name": "ddo-data-images", 
        # "path": "c:/github/ddo-data-images", 
        # "url": "https://github.customerlabs.com.au/iagcl/ddo-data-images.git", 
        if repo['name']:
            break
        elif cnt > 2:
            cutie.cprint('error', "try failed, exit")
            cutie.get_exit()
        else:
            cutie.cprint('error', "invalid url, must contain .git")

    path = cutie.linux_path(cutie.get_input(cc.value('project', 'path_message')))
    repo["path"] = path
    if not repo["connection-ssh"]:
        user = cutie.get_input(cc.value('project', 'user_message'))
        password = cutie.get_pass(cc.value('project', 'password_message'))
    repo["up-stream"] = "" 
    repo["version"]= cutie.get_input("Latest Tag Version (x.x.x) format:")
    repo["task"] = cutie.get_input("task branch prefix (CLD- ):")
    repo["hotfix"]= cutie.get_input("hotfix branch prefix (HFX- ):") 
    repo["is-current"] = False 
    repo["git-flow"] = True 
    repo["descption"]= "" 
    repo["jira-link"]= "" 
    repo["issue"]= "" 
    
    # if cddir(path) :
    if cutie.prompt_yn(cc.value('project', 'gitclone_message').format(repo['url'], path)):
        cutie.cprint('wait', cc.value('git-talk', 'wait'))
        try:
            created = False
            if not os.path.exists(path):
                os.mkdir(path)
              
            # cutie.cprint('info','my_repositories',repo['repo'],path)
            # To save credentials you can clone Git repository by setting a username and password on the command line:
            # https://www.shellhacks.com/git-config-username-password-store-credentials/
            if not repo["connection-ssh"]:
                git_url_user_password = repo['url'].replace(
                    "://", "://" + user + ":" + password + "@")
            else:
                git_url_user_password = repo['url']

            command = [['git','clone', git_url_user_password]]
            b, _ = gfunc.subprocess_cmd(path,command)
            # b = gfunc.execute_git_command(
            #     path, 'clone {0}'.format(git_url_user_password))
            
            created = True
            # else:
            #     if prompt_yn(cc.value('project','gitclone_existing').format(repo['url'],path)):
            #         created = True
            if created:        
                repo["path"] = cutie.linux_path(os.path.join(path, repo["name"]))
                #gitflow(repo["path"], cc)
                # rp = repo["path"] + "|" + repo["url"] + "|VERSION=0.0.0"
                cc.save_json('repo_json', repo["name"], repo)

                cutie.cprint('done', cc.value('git-talk', 'done'))
                repo["branch"] = branches.pick_branch(cc, repo)
        except Exception as e:
            cutie.cprint('error', str(e))
            cutie.cprint('error', cc.value('git-talk', 'error'))
            cutie.get_exit()
        else:
            cutie.get_exit()
    else:
        cutie.get_exit()
    return repo
    # print(cc.value('project','project_path').format(branch,path))
