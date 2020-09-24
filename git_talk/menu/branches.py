import os
import csv
import time
import json
# from git_talk import __version__
import git_talk.lib.gfunc as gfunc
import git_talk.lib.cutie as cutie
import git_talk.lib.changelog.main as changelog
import git_talk.menu.status as stts 


def pick_branch(cc, repo):
    
    path = repo['path']
    cc.save("access","current_repo", repo["name"])
    command =[['git','branch']]
    b,error = gfunc. subprocess_cmd(path, command)
    selected_branch = ''
    working_list = []
    for ib in b[0].split('\n'):
        if ib.strip():
            if ib.strip().startswith('*'):
                selected_branch = ib.strip().replace('*', '')
            if ib.strip().replace('*', '') not in ('master', 'dev', 'release'):
                working_list.append(ib)
    create_b = cc.value("branch", "create_branch")
    working_list.append(create_b)
    delete_b = cc.value("branch", "close_branch")
    working_list.append(delete_b)

    name = cutie.select_propmt(cc.value('project', 'branch'),
                         working_list).replace('*', '').strip()
    if not cutie.get_exit(name):
        # TODO: will config prefix_ ,created by xxxxx and linked issue or jira
        if name == create_b:
            br_type = {'feature': repo["task"], 'hotfix': repo["hotfix"]}
            ty = cutie.select_propmt(cc.value('branch', 'branch_type'), [
                               'feature', 'hotfix']).strip()
            if not cutie.get_exit(ty):
                if ty == 'hotfix':
                    nb_from = 'master'
                else:
                    nb_from = 'dev'

                nb = cutie.get_input(cc.value('branch', 'new_branch'))
                nb = br_type[ty] + nb
                cutie.cprint('info', 'creating {0} branch: {1}'.format(ty, nb))
                if nb not in b:
                    cmd_branch = [["git", "checkout", nb_from], [
                        "git", "pull"], ["git", "checkout", "-b", nb],["git","push","--set-upstream", "origin", nb]]
                    b, error = gfunc.subprocess_cmd(path, cmd_branch)
                    if error == 0:
                        selected_branch = nb
                    else:
                        cutie.cprint('error', cc.value('git-talk', 'error'))

                    # b = gfunc. subprocess_cmd(path, 'checkout {0}'.format(nb_from))
                    # b = gfunc. subprocess_cmd(path, 'checkout -b {0}'.format(nb))
                else:
                    cutie.cprint('alarm', cc.value(
                    'branch', 'existing_branch').fromat(nb))
        elif name == delete_b:
            command = [["git", "branch"]]
            b, error = gfunc.subprocess_cmd(repo['path'], command)
            if error == 0:
                ty = cutie.select_propmt(
                    cc.value('branch', 'close_picked'), b[0].split('\n')).strip()
                if not cutie.get_exit(ty):
                    if '*' in ty:
                        cutie.cprint('alarm', cc.value(
                            'branch', 'current_alarm'))
                    else:
                        b, error = gfunc.subprocess_cmd(repo['path'], [["git", "branch", "-d", ty]])
                        if error == 1 :
                            if cutie.prompt_yn(cc.value('branch', 'confirm_delete').format(ty)):
                                b, error = gfunc.subprocess_cmd(repo['path'], [["git", "branch", "-D", ty]])
                                if error == 0 :
                                    b, error = gfunc.subprocess_cmd(repo['path'], [["git", "push", "origin", "--delete",ty]])
                        else:
                            b, error = gfunc.subprocess_cmd(repo['path'], [["git", "push", "origin", "--delete",ty]])
        else:
            # checkout the branch
            if name != selected_branch:
                command =[['git','checkout', name]]
                bb,error = gfunc. subprocess_cmd(path,command )
                if error == 0:
                    cutie.cprint('info', cc.value(
                        'project', 'checkout').format(name))
                    selected_branch = name
                else:
                    cutie.cprint('error', bb + '------------\n error:', str(error))
                    cutie.cprint('info', cc.value('project', 'checkout_error').format(name))
                    cutie.cprint('error', cc.value('git-talk', 'error'))

    repo['branch'] = selected_branch
    cc.save_json("repo_json", repo["name"], repo)
    return repo

def del_branch_tag(cc, repo):
    # git branch -d branch_name (first)
    # if confirmed -D (remove)
    # git push origin :branch_name
    pass


'''
get VERSION from config. A.B.C, will tag on PR 
    A = (major) manual, B= (minor) manual, C=(micro) bugfix/feature PR auto +1 
'''


def add_tag(cc, repo):
    error = "no defined error"
    current_branch, remote_status = stts.current_status(repo)
    command = [["git", "checkout", "master"]]
    b, error = gfunc.subprocess_cmd(repo['path'], command)
    #j = control_package(cc,repo["path"])
    version = cutie.get_input(
        cc.value('pr', 'tag').format(repo["version"]))
    comment = cutie.get_input(cc.value('commit', 'comment')) 
    if len(version) >= 5  and version.count(".") == 2 :
        repo["version"] = version
        #control_package(cc,repo["path"], j)

        command = [["git","add",".","&&","git","commit","-m",'"tag version bump up"'],["git", "checkout", "dev","&&", "git", "pull"],
                    ["git", "checkout", "master","&&", "git", "pull"],
                    ["git", "merge", "dev"], 
                    ["git", "tag", "-a", version, "-m", '"' + comment + '"'],
                    ["git","push","origin","--tag"]]
        cutie.cprint('info', 'creating tag {} and its changelog.md, please wait...'.format(version))
        b, error = gfunc.subprocess_cmd(repo['path'], command)
        
        changelog.main(repo = repo["path"], description=comment ,latest_version= version )

        # auto-changelog -p && git add CHANGELOG.md
        command = [["git","add","."],["git", "commit", "-m", "'Others: version bump to: " + version + "'"], 
                   ["git", "push", "origin","HEAD:master"]]
        b, error = gfunc.subprocess_cmd(repo['path'], command)
        #menu.bumper_changelog(cc,repo)
        # repo['version'] = version
        # rp = cc.value('my_repositories', repo["name"]).split(
        #         "VERSION=")[0] + "VERSION=" + version
        # cc.save('current_repo', repo["name"], rp)
        cc.save_json("repo_json",repo["name"],repo)
    else:
        pass
    command = [["git","checkout",current_branch]]
    b, error = gfunc.subprocess_cmd(repo['path'], command)
    return error
    # git tag -a v1.4 -m "my version 1.4"

def branch_manager(cc, repo, path, action='list-all', name=''):
    # list all branch
    if action == 'list-all':
        return gfunc. subprocess_cmd(path, [['git','branch']])
    # list working branch
    elif action == 'list-work':
        return gfunc. subprocess_cmd(path, [['git',"branch | grep | grep 'hfx\|tsk'_* "]])
    # create branch
    elif action == 'create':
        pass
    # sync remote/local branch
    elif action == 'sync':
        pass
    # remove branch from remote/local
    elif action == '':
        pass

