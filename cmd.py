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
import git_talk.lib.gfunc as gfunc
import git_talk.lib.cutie as cutie
import git_talk.lib.config as config
import git_talk.lib.github_api as github_api
import git_talk.lib.changelog.main as changelog
import git_talk.menu.projects as projects
import git_talk.menu.status as stts
import git_talk.menu.rebase as rebase
import git_talk.menu.graph as graph
import git_talk.menu.branches as branches
import git_talk.menu.commit as commit
import git_talk.menu.pr as pr


'''
TODO: 
add tag for VERSION when PR
graph display (master, hfx_x, release, dev, tsk_x)
'''

def main():
    cc = config.conf('.git_talk.ini')
    cutie.cprint('info', cc.value('git-talk', 'welcome'))

    if not cc.value('access', 'git_api'):
        cutie.cprint('blank', '')
        git_api = cutie.get_input(cc.value('git-talk', 'git_api_message'))
        if not git_api:
            git_api = 'https://github.com.au/api/v3'
        cutie.cprint('alarm', cc.value('git-talk', 'token_help_message'))
        cutie.cprint('', '')
        token = cutie.get_input(cc.value('git-talk', 'token_message'))
        g = github_api.GitHubAPI(git_api=git_api, token=token)
        if g is not None:
            cc.save("access", "git_api", git_api)
            cc.save("access", "token", token)
        else:
            cutie.cprint('error', "invalid api or token.")
            if cutie.get_exit(value='Exit', ex=True, message=m):
                exit()
    repo = {}
    user_git_repo_list = [i for i in cc.values_json('repo_json')]
    for r in user_git_repo_list:
        for k, v in r.items():
            if k == cc.value("access", "current_repo"):
                repo = v 
    if not repo:
        repo = projects.create_project(cc)

    # g.init(repo)

    while True:
        names = cc.value('git-talk', 'steps').split(',')
        b, status = stts.current_status(repo)
        if status == 1:
            break
        repo["branch"] = b
        msg = cc.value('git-talk', 'message').format(repo["name"], b, status)
        name = cutie.select_propmt(msg, names, exit='Exit')
        #name = cutie.select_propmt(cc.value('git-talk','message'),names)
        #names = cc.value('git-talk','steps').split(',')
        if name == names[0]:
            graph.git_simple(cc, repo)
        elif name == names[1]:
            r = projects.project(cc)
            if r is not None:
                repo = r
        elif name == names[2]:
            rebase.rebase(cc, repo)
        elif name == names[3]:
            pr_tag_release(cc, repo)
        elif name == names[4]:
            branches.pick_branch(cc, repo)
        elif name == names[5]:
            commit.commit(cc, repo)
        elif name == names[6]:
            m = 'Exit git-talk CLI gracefully!'
            if cutie.get_exit(value=name, ex=True, message=m):
                break
        # time.sleep(1)


def pr_tag_release(cc, repo):
    while True:
        names = cc.value('pr-tag-release', 'steps').split(',')
        b, status = stts.current_status(repo)
        if status == 1:
            break
        msg = cc.value('git-talk', 'message').format(repo["name"], b, status)
        name = cutie.select_propmt(msg, names)
        if name == names[0]:
            pr.pr(cc,repo)
        elif name == names[1]:
            branches.add_tag(cc,repo)
        # elif name == names[2]:
        #     pass
        #     #merge_tag_master(cc,repo)
        elif name == names[2]:
            m = 'back to upper menu'
            if cutie.get_exit(value=name, ex=False, message=m):
                break


if __name__ == '__main__':
    main()