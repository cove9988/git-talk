import os
import csv
import time

# from git_talk import __version__
import git_talk.lib as lib
import git_talk.menu as menu 

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
    name = lib.cutie.select_propmt(lns, names)
    name = name[:PROJECT_SPACE-1].strip()
    if name == create_msg:
        repo = create_project(cc)
    elif name == 'Exit':
        lib.cutie.get_exit()
        return None
    else:
        for r in user_git_repo_list:
            for k, v in r.items():
                if name == k :
                    repo = v
                    menu.pick_branch(cc, repo)
                    cc.save_json('repo_json',repo["name"], repo )
    return repo

def create_project(cc):
    repo = {}
    # if prompt_yn(cc.value('project','create_doyou')):
    # input directory and git clone
    #pro = cutie.get_input(cc.value('project','project_name'))
    cnt = 0
    ssh_repo = False
    user,password = '',''   
    if (lib.cutie.prompt_yn("Do you use ssh connect to repository?")):
        repo["connection-ssh"] = True
    else :
        repo["connection-ssh"] = False

    while True:
        cnt += 1
        repo['url'] = lib.cutie.get_input(cc.value('project', 'project_url'))
        repo['name'] = menu.get_repo_name(url=repo['url'])
        if repo['name']:
            break
        elif cnt > 2:
            lib.cutie.cprint('error', "try failed, exit")
            lib.cutie.get_exit()
        else:
            lib.cutie.cprint('error', "invalid url, must contain .git")

    path = lib.cutie.linux_path(lib.cutie.get_input(cc.value('project', 'path_message')))
    repo["path"] = path
    if not ssh_repo:
        user = lib.cutie.get_input(cc.value('project', 'user_message'))
        password = lib.cutie.get_pass(cc.value('project', 'password_message'))
    # if cddir(path) :
    if lib.cutie.prompt_yn(cc.value('project', 'gitclone_message').format(repo['url'], path)):
        lib.cutie.cprint('wait', cc.value('git-talk', 'wait'))
        try:
            created = False
            if not os.path.exists(path):
                os.mkdir(path)
              
            # cutie.cprint('info','my_repositories',repo['repo'],path)
            # To save credentials you can clone Git repository by setting a username and password on the command line:
            # https://www.shellhacks.com/git-config-username-password-store-credentials/
            if not ssh_repo:
                git_url_user_password = repo['url'].replace(
                    "://", "://" + user + ":" + password + "@")
            else:
                git_url_user_password = repo['url']

            #command = ['git','clone', git_url_user_password ]
            #b, _ = gfunc.subprocess_cmd(path,command)
            b = lib.gfunc.execute_git_command(
                path, 'clone {0}'.format(git_url_user_password))
            created = True
            # else:
            #     if prompt_yn(cc.value('project','gitclone_existing').format(repo['url'],path)):
            #         created = True
            if created:        
                repo["path"] = lib.cutie.linux_path(os.path.join(path, repo["name"]))
                #gitflow(repo["path"], cc)
                # rp = repo["path"] + "|" + repo["url"] + "|VERSION=0.0.0"
                cc.save_sjon('repo_json', repo["name"], repo)

                lib.cutie.cprint('done', cc.value('git-talk', 'done'))
                repo["branch"] = menu.pick_branch(cc, repo)
        except Exception as e:
            lib.cutie.cprint('error', str(e))
            lib.cutie.cprint('error', cc.value('git-talk', 'error'))
            lib.cutie.get_exit()
        else:
            lib.cutie.get_exit()
    else:
        lib.cutie.get_exit()
    return repo
    # print(cc.value('project','project_path').format(branch,path))
