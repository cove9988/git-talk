
import git_talk.lib.gfunc as gfunc
import git_talk.lib.cutie as cutie

def commit(cc, repo, comment = "", up_stream="origin"):
    if repo['branch'] in ('master'):
        cutie.cprint(
            'alert', (cc.value('commit', 'error').format(repo['branch'])))
    else:
        summary = ''
        names = cc.value('commit','commit_prefix').strip().split(",")
        while len(summary) < 1:
            summary = cutie.select_propmt(cc.value('commit','summary'), names)
            if summary.lower() in ('exit', 'cancel'):
                cutie.get_exit()
                return None
        while len(comment) < 1:
            comment = cutie.get_input(cc.value('commit', 'comment'))
        comment = summary + ': ' + comment
        cutie.cprint('wait', (cc.value('git-talk', 'wait')))
        path = repo['path']
        # git_path = "C:/Program Files/Git/cmd/git.exe"
        command = [["git", "add", "."], 
                    ["git", "commit", "-m", comment], 
                    ["git", "pull", up_stream], 
                    ["git", "push", "-u", up_stream, repo['branch'].strip()]]
        b, error = gfunc.subprocess_cmd(path, command)

