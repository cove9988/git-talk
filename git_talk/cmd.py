#! /usr/bin/env python3

import os
import csv


from git_talk import __version__
import git_talk.lib.gfunc as gfunc
import git_talk.lib.cutie as cutie
import git_talk.lib.config as config
import git_talk.lib.github_api as github_api


#repo ={url:x, path:y, branch:z, repo:a}
def main():
    cc = config.conf('.git_talk.ini')
    cutie.cprint('alarm',cc.value('git-talk','welcome'))

    if not cc.value('access','git_api'):
        cutie.cprint('blank','')
        git_api = cutie.get_input(cc.value('git-talk','git_api_message'))
        if not git_api:
            git_api = 'https://github.com.au/api/v3'
        cutie.cprint('alarm',cc.value('git-talk','token_help_message'))
        cutie.cprint('','')
        token = cutie.get_input(cc.value('git-talk','token_message'))
        g = github_api.GitHubAPI(git_api=git_api, token = token)
        if g is not None:
            cc.save("access","git_api",git_api)
            cc.save("access","token",token)
        else:
            cutie.cprint('error',"invalid api or token.")
            if cutie.get_exit(value='Exit', ex=True,message=m):
                exit()
    repo ={}
    if cc.value('current_project','url'):
        repo['url']= cc.value('current_project','url')
        repo['path']= cc.value('current_project','path')
        repo['branch']= cc.value('current_project','branch')
        repo['repo']= cc.value('current_project','repo')
    else:
        repo = projects(cc)
    
    #g.init(repo)

    while True:
        names = cc.value('git-talk','steps').split(',')
        msg = cc.value('git-talk','message').format(repo["repo"], repo["branch"])
        name = select_propmt(msg,names)
        #name = select_propmt(cc.value('git-talk','message'),names)
        #names = cc.value('git-talk','steps').split(',')
        if name == names[0]:
            repo = projects(cc)
        elif name == names[1]:
            rebase(cc)
        elif name == names[2]:
            commit(cc,repo)
        elif name == names[3]:
            load(cc)
        elif name == names[4]:
            pr(cc,repo)
        else:
            m = 'Exit git-talk CLI gracefully!'
            if cutie.get_exit(value=name, ex=True,message=m):
                break

def projects(cc):
    user_git_repo_list = [i for i in cc.values('my_repositories')]

    names =[]
    repos =[]
    repo ={}
    create_msg = cc.value('project','create_message')
    for r in user_git_repo_list:
        for k,v in r.items():
            p,r = [v.split('|')[i] for i in (0,1)]
            n = "{:<40}".format(k)  + p
            names.append(n)
            rp = {n:{"url":r,"path":p}}
            repos.append(rp)
    names.append(create_msg) 

    lns =cc.value('project','branch') + "\n{:<44}".format("    Project ") + "Path"
    name = select_propmt(lns,names)
    if name == create_msg:
        repo = create_project(cc)
    elif name == 'Exit':
        m = 'Exit git-talk CLI gracefully!'
        cutie.get_exit(value='Exit', ex=True, message=m )
    else:
        for ip in repos:
            if name in ip.keys():
                selected_path = ip[name]["path"]
                selected_url = ip[name]["url"]
                selected_repo = get_repo_name(path=selected_path)
                selected_branch = pick_branch(selected_path,cc)
                repo ={'url':selected_url, 'path':selected_path,'repo':selected_repo,'branch':selected_branch }
    if repo["url"]:
        cc.save("current_project","url",repo["url"])
        cc.save("current_project","branch",repo["branch"])
        cc.save("current_project","path",repo["path"])
        cc.save("current_project","repo",repo["repo"])
    
    return repo

def create_project(cc):
    repo = {}
    #if prompt_yn(cc.value('project','create_doyou')):
    #input directory and git clone
    #pro = cutie.get_input(cc.value('project','project_name'))
    while True:
        repo['url'] = cutie.get_input(cc.value('project','project_url'))
        repo['repo'] = get_repo_name(url = repo['url'])
        if repo['repo']:
            break
        else:
            cutie.cprint('error',"invalid url, must contain .git")

    path = linux_path(cutie.get_input(cc.value('project','path_message')))
    user = cutie.get_input(cc.value('project','user_message'))
    password = cutie.get_input(cc.value('project','password_message'))
    #if cddir(path) : 
    if prompt_yn(cc.value('project','gitclone_message').format(repo['url'], path)):
        cutie.cprint('wait',cc.value('git-talk','wait'))
        try:
            if not os.path.exists(path):
                os.mkdir(path)

            #cutie.cprint('info','my_repositories',repo['repo'],path)
            # To save credentials you can clone Git repository by setting a username and password on the command line:
            # https://www.shellhacks.com/git-config-username-password-store-credentials/
            git_url_user_password = repo['url'].replace("://","://" + user + ":" + password + "@")
            #command = ['git','clone', git_url_user_password ]
            #b = gfunc.subprocess_cmd(path,command)
            b = gfunc.execute_git_command(path, 'clone {0}'.format(git_url_user_password)) 
            repo["path"] = linux_path(os.path.join(path,repo["repo"]))

            rp = repo["path"] + "|" + repo["url"]
            cc.save('my_repositories',repo["repo"],rp)
            cutie.cprint('done', cc.value('git-talk','done'))
            repo["branch"] = pick_branch(repo["path"],cc)
        except Exception as e:
            cutie.cprint('error',str(e))
            cutie.cprint('error',cc.value('git-talk','error'))
            cutie.get_exit()
        else:
            cutie.get_exit()
    # else:
    #     cutie.get_exit()
    return repo
    #print(cc.value('project','project_path').format(branch,path))

def pick_branch(path, cc): 
    b = gfunc.execute_git_command(path, 'branch')
    selected_branch =''
    for ib in b:
        if ib.strip().startswith('*'):
            selected_branch = ib.strip().replace('*','')
    
    cb = cc.value("branch","create_message")
    b.append(cb)
    
    name = select_propmt(cc.value('project','branch'),b).replace('*','')
    if not cutie.get_exit(name):
        if name == cb:
            nb = cutie.get_input(cc.value('branch','new_branch'))
            if nb not in b:
                b = gfunc.execute_git_command(path, 'checkout -b {0}'.format(nb))
                selected_branch = nb
            else:
                cprint('alarm',cc.value('branch','existing_branch').fromat(nb))
        else:
            #checkout the branch
            if name != selected_branch:
                bb = gfunc.execute_git_command(path, 'checkout {0}'.format(name))
                if bb :
                    cutie.cprint('info',cc.value('project','checkout').format(name))
                    selected_branch = name
                else:
                    cutie.cprint('info',cc.value('project','checkout_error').format(name))
                    cutie.cprint('error',cc.value('git-talk','error'))
    return selected_branch

def rebase(cc):
    # TODO: rebase
    cutie.cprint('error',cc.value('git-talk','error'))

def del_branch_tag(cc,repo):
    # git branch -D branch_name
    # git push origin :branch_name
    pass
def add_tag(cc,repo):
    # git tag -a v1.4 -m "my version 1.4"
    pass

def commit(cc,repo):
    # summary = ''
    comment = ''
    # while len(summary) < 1:
    #     summary = cutie.get_input(cc.value('commit','summary'))
    while len(comment)<1:
        comment = cutie.get_input(cc.value('commit','comment'))
    # comment = summary.upper() + '\n\n' + comment
    cutie.cprint('wait',(cc.value('git-talk','wait')))
    path = repo['path']
    git_path = "C:/Program Files/Git/cmd/git.exe"

    command =[["git", "add","." ],["git","status"],["git","commit","-m",'"' + comment + '"'],["git", "pull", "origin"],["git", "push", "-u", "origin", repo['branch'].strip()]]
    b = gfunc.subprocess_cmd(path,command)
  
def load(cc):
    # TODO: loop throught main blocks save data to csv
    view = cutie.get_input(cc.value('load','whichview'))
    cutie.cprint('info',cc.value('git-talk','wait'))
    ld = load_dataset.LoadData(view)
    error = ld.get_objects()
    if error == 0:
        #stmt, obj_list = load_dataset.get_objects(view)
        if ld.obj_list is not None:
            captions =[0]
            cutie.cprint('info',cc.value('load','pick_main_table'))
            main_obj = select_propmt(cc.value('load','object_list'), ld.obj_list,captions)
            if not cutie.get_exit(main_obj):
                rd_cnt = cutie.get_number(cc.value('load','how_many'),min_value = 1, allow_float=False)
                cutie.cprint('wait',(cc.value('git-talk','wait')))
                #run main_obj first, then loop rest
                cutie.cprint('info',(ld.build_sql))
                #TODO: save into csv
                mtb = main_obj.strip().split(' ')[0]
                r = ld.get_result(mtb,rd_cnt) 
                f = mtb + '.csv'
                with open(f, 'w') as c:
                    wr = csv.writer(c)
                    wr.writerow(r)
                    cutie.cprint('info',('write into ',f))
                cutie.cprint('info',mtb, '--row count--->',len(r))
                # print(r[0])
                cutie.cprint('done',(cc.value('git-talk','done')))        
    else:
        cutie.cprint('alarm',cc.value('load','no_table'))
        # cutie.get_exit()

def pr(cc,repo):
    # TODO: squash commit, list from and into branches (both local and remote). if need, notify codereviewer.
    cutie.cprint('wait',(cc.value('git-talk','wait')))
    cutie.cprint('','')
    gh = github_api.GitHubAPI( cc.value('access','git_api'), cc.value('access','token'))
    gh.set_repo(repo['url'])
    title = cutie.get_input(cc.value('pr','title'))
    #summary = cutie.get_input(cc.value('pr','summary'))
    detail  = cutie.get_input(cc.value('pr','detail'))
    #detail = summary.upper() + '\n' + detail
    
    b = gfunc.execute_git_command(repo['path'], 'branch')
    head = select_propmt(cc.value('pr','head'),b).replace('*','')
    base = select_propmt(cc.value('pr','base'),b).replace('*','')
    head = head.strip()
    base = base.strip()
    if head == base:
        cutie.cprint('error',(cc.value('git-talk','error')))
    else:
        pr = gh.pull_request(title, detail,head,base)
        if pr is None:
            cutie.cprint('error',(cc.value('git-talk','error')))
        else:
            cutie.cprint('info',(cc.value('git-talk','done'))) 

def prompt_yn(message):
    #message = '\n' + message
    return cutie.prompt_yes_or_no(message)

def select_propmt(message,names,captions=[]):
    cutie.cprint('alert',('\n' + message))
    captions =[]
    # List of names to select from, including some captions
    # Names which are captions and thus not selectable
    # captions = [0, 2, 7]
    # Get the name
    if 'Exit' not in names:
        names.append('Exit') 
    name = names[
        cutie.select(names, caption_indices=captions, selected_index=len(names))]

    return name

def get_repo_name(url ='', path=''):
    repo_name=''
    if url:
        url_part = url.split("/")
        g= url_part[-1].split(".")
        if g[-1] == 'git':
            repo_name = g[0]        
    if path:
        path = path.replace('\\','/')
        repo_name = path.split('/')[-1]
    return repo_name

def linux_path(path):
    return path.replace("\\","/")

if __name__ == '__main__':
    main()