import git_talk.lib.gfunc as gfunc
import git_talk.lib.cutie as cutie

def get_repo_name(url='', path=''):
    repo_name = ''
    if url:
        url_part = url.split("/")
        g = url_part[-1].split(".")
        if g[-1] == 'git':
            repo_name = g[0]
    if path:
        path = path.replace('\\', '/')
        repo_name = path.split('/')[-1]
    return repo_name


def current_status(repo):
    # cutie.cprint('wait', 'updating the git status...')
    command = [["git","fetch","--all"],["git", "status", "-v", "-s", "-b"]]
    b, error = gfunc.subprocess_cmd(repo['path'], command, display=False)
    if error == 0:
        #  result windows   ## dev...origin/dev [behind/head 2] or nothing if equal, not []
        #                   M git_talk/cmd.py --------> if head
        #                   blank line
        
        rs = b[1].split("\n")
        for i, r in enumerate(rs):
            if i == 0:
                current_branch, remote_status = '',''
                if "..." not in r : #no remote branch
                    current_branch = r
                else:
                    current_branch, remote_status = r.split("...")

                current_branch = current_branch.replace("##", "").strip()
                if "[" in remote_status:
                    remote_status ="[" + remote_status.split(
                        "[")[-1].split("]")[0].strip() +"]"
                else:
                    remote_status = "[=]"

        return current_branch, remote_status
    else:
        print(b)
        return "error", error
