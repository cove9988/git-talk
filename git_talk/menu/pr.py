import git_talk.lib as lib
import git_talk.menu as menu

def pr(cc, repo):
    # squash commit, list from and into branches (both local and remote). if need, notify codereviewer.
    base = ''
    lib.cutie.cprint('wait', (cc.value('git-talk', 'wait')))
    lib.cutie.cprint('', '')
    gh = lib.github_api.GitHubAPI(
        cc.value('access', 'git_api'), cc.value('access', 'token'))
    gh.set_repo(repo['url'])
    current_b, status = menu.current_status(repo)
    b = lib.gfunc.execute_git_command(repo['path'], 'branch')
    head = lib.cutie.select_propmt(cc.value('pr', 'head'), b).replace('*', '')
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
        lib.cutie.cprint('error', (cc.value('git-talk', 'error')))
    else:
        title = lib.cutie.get_input(cc.value('pr', 'title'))
        #summary = cutie.get_input(cc.value('pr','summary'))
        detail = lib.cutie.get_input(cc.value('pr', 'detail'))
        #detail = summary.upper() + '\n' + detail
        pr = gh.pull_request(title, detail, head, base)
        if pr is None:
            lib.cutie.cprint('error', (cc.value('git-talk', 'error')))
        else:
            lib.cutie.cprint('info', (cc.value('pr', 'done').format(base, head)))

    b = lib.gfunc.subprocess_cmd(repo['path'], [["git","checkout",current_b]])
