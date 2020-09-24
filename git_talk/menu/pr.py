import git_talk.lib.gfunc as gfunc
import git_talk.lib.cutie as cutie
import git_talk.lib.github_api as github_api
import git_talk.menu.status as stts

def pr(cc, repo):
    # squash commit, list from and into branches (both local and remote). if need, notify codereviewer.
    base = ''
    cutie.cprint('wait', (cc.value('git-talk', 'wait')))
    cutie.cprint('', '')
    gh = github_api.GitHubAPI(
        cc.value('access', 'git_api'), cc.value('access', 'token'))
    gh.set_repo(repo['url'])
    current_b, status = stts.current_status(repo)
    b = gfunc.execute_git_command(repo['path'], 'branch')
    head = cutie.select_propmt(cc.value('pr', 'head'), b).replace('*', '')
    head = head.strip()
    if head.startswith(repo["task"]):
        base = 'dev'
    elif head.startswith(repo["hotfix"]):
        base = 'master'
    
        
    #elif head == 'dev':
    #    base = 'release'
    #elif head == 'release':
    #    base = 'master'
    #else:
    #    base = ''
    #base = cutie.select_propmt(cc.value('pr','base'),b).replace('*','')
    base = base.strip()
    if head == base or base == '':
        cutie.cprint('error', (cc.value('git-talk', 'error')))
    else:
        title = cutie.get_input(cc.value('pr', 'title'))
        #summary = cutie.get_input(cc.value('pr','summary'))
        detail = cutie.get_input(cc.value('pr', 'detail'))
        #detail = summary.upper() + '\n' + detail
        pr = gh.pull_request(title, detail, head, base)
        if pr is None:
            cutie.cprint('error', (cc.value('git-talk', 'error')))
        else:
            cutie.cprint('info', (cc.value('pr', 'done').format(base, head)))

    b = gfunc.subprocess_cmd(repo['path'], [["git","checkout",current_b]])
