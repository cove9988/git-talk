import os
import csv
import time

import git_talk.lib.gfunc as gfunc
import git_talk.lib.cutie as cutie

def rebase(cc, repo):
    cutie.cprint('wait', (cc.value('git-talk', 'wait')))
    # get all branch from remote
    cutie.cprint('info', cc.value('rebase', 'remote_branch'))
    get_all_remote_brancb = [["git", "branch", "--all"]]

    b, error = gfunc.subprocess_cmd(repo['path'], get_all_remote_brancb)
    # clean the branch, remove * remotes
    if error == 1:
        return

    bs = b[0].split('\n')
    local_branches = []
    remote_branches = []
    current_branch = ''
    for i in bs:
        if '*' in i:
            i = i.replace('*', '')
            current_branch = i.strip()
        i = i.strip()
        if 'remotes/' in i:
            remote_branches.append(i.replace('remotes/', ''))
        else:
            local_branches.append(i)
    for i in remote_branches:
        local = i.split('/')[-1]
        if local not in local_branches:
            cutie.cprint('info', cc.value('rebase', 'no_local').format(i))
            remote_branch = [["git", "branch", "--track", local, i]]
            b, error = gfunc.subprocess_cmd(repo['path'], remote_branch)
        else:
            cutie.cprint('info', cc.value('rebase', 'pull').format(local))
            remote_branch = [["git", "checkout", local], ["git", "pull"]]
            b, error = gfunc.subprocess_cmd(repo['path'], remote_branch)
        if error == 1:
            break
    # merge master
    if error == 0:
        git_pull = [["git", "checkout", "dev"], ["git", "merge", "master"], [
            "git", "push"], ["git", "checkout", current_branch]]
    # ["git","merge","master"],["git", "push"]]
        b, error = gfunc.subprocess_cmd(repo['path'], git_pull)

    #print(remote_branches, local_branches)
    # cutie.cprint('info',cc.value('git-talk','error'))
    return error

