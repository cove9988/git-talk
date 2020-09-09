#! /usr/bin/env python3
'''
TODO LIST:
1. release tag with build changelog.md
2. if the clone folder exist with git, ask to configure.
3. changelog for tagv https://stackoverflow.com/questions/7387612/git-changelog-how-to-get-all-changes-up-to-a-specific-tag 
   use git shortlog v1..v2 diff 
4. web version
5. screen animation
6. link with issue or jira
7. better rebase

'''
import os
import csv
import time

# from git_talk import __version__
import git_talk.lib as lib
import git_talk.menu as menu

'''
TODO: 
add tag for VERSION when PR
graph display (master, hfx_x, release, dev, tsk_x)
'''

def main():
    cc = lib.config.conf('.git_talk.ini')
    lib.cutie.cprint('info', cc.value('git-talk', 'welcome'))

    if not cc.value('access', 'git_api'):
        lib.cutie.cprint('blank', '')
        git_api = lib.cutie.get_input(cc.value('git-talk', 'git_api_message'))
        if not git_api:
            git_api = 'https://github.com.au/api/v3'
        lib.cutie.cprint('alarm', cc.value('git-talk', 'token_help_message'))
        lib.cutie.cprint('', '')
        token = lib.cutie.get_input(cc.value('git-talk', 'token_message'))
        g = lib.github_api.GitHubAPI(git_api=git_api, token=token)
        if g is not None:
            cc.save("access", "git_api", git_api)
            cc.save("access", "token", token)
        else:
            lib.cutie.cprint('error', "invalid api or token.")
            if lib.cutie.get_exit(value='Exit', ex=True, message=m):
                exit()
    repo = {}
    user_git_repo_list = [i for i in cc.values_json('repo_json')]
    for r in user_git_repo_list:
        for k, v in r.items():
            if k == cc.value("access", "current_repo"):
                repo = v 
    if not repo:
        repo = menu.project(cc)

    # g.init(repo)

    while True:
        names = cc.value('git-talk', 'steps').split(',')
        b, status = menu.current_status(repo)
        if status == 1:
            break
        repo["branch"] = b
        msg = cc.value('git-talk', 'message').format(repo["name"], b, status)
        name = lib.cutie.select_propmt(msg, names)
        #name = cutie.select_propmt(cc.value('git-talk','message'),names)
        #names = cc.value('git-talk','steps').split(',')
        if name == names[0]:
            menu.git_simple(cc, repo)
        elif name == names[1]:
            r = menu.project(cc)
            if r is not None:
                repo = r
        elif name == names[2]:
            menu.rebase(cc, repo)
        elif name == names[3]:
            pr_tag_release(cc, repo)
        elif name == names[4]:
            menu.pick_branch(cc, repo)
        elif name == names[5]:
            menu.commit(cc, repo)
        elif name == names[6]:
            m = 'Exit git-talk CLI gracefully!'
            if lib.cutie.get_exit(value=name, ex=True, message=m):
                break
        # time.sleep(1)


def pr_tag_release(cc, repo):
    while True:
        names = cc.value('pr-tag-release', 'steps').split(',')
        b, status = menu.current_status(repo)
        if status == 1:
            break
        msg = cc.value('git-talk', 'message').format(repo["name"], b, status)
        name = lib.cutie.select_propmt(msg, names)
        if name == names[0]:
            menu.pr(cc,repo)
        elif name == names[1]:
            menu.add_tag(cc,repo)
        # elif name == names[2]:
        #     pass
        #     #merge_tag_master(cc,repo)
        elif name == names[2]:
            m = 'back to upper menu'
            if lib.cutie.get_exit(value=name, ex=False, message=m):
                break


if __name__ == '__main__':
    main()