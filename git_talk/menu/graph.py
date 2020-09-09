import re
import git_talk.lib as lib
import git_talk.menu as menu
def gitflow(cc, repo):
    '''
    create gitflow structure
    master=prod,release=release,dev=dev,hotfix=hotfix,feature=feature 
    '''
    #
    # git config --global alias.hist "log --graph --date-order --date=short --pretty=format:'%C(auto)%h%d %C(reset)%s %C(bold blue)%ce %C(reset)%C(green)%cr (%cd)'"

    #Usage:
    # git hist - Show the history of current branch
    # git hist --all - Show the graph of all branches (including remotes)
    # git hist master devel - Show the relationship between two or more branches
    # git hist --branches - Show all local branches

    # Add --topo-order to sort commits topologically, instead of by date (default in this alias)

    # Benefits:
    # Looks just like plain --decorate, so with separate colors for different branch names
    # Adds committer email
    # Adds commit relative and absolute date
    # Sorts commits by date
    # Setup:
    
    cmd = [["git", "hist", "--branches"]]

    b, error = lib.gfunc.subprocess_cmd(repo['path'], cmd)
    # print(b)

def git_graph(cc, repo, time):
    # [alias]
    # good one lg1 = git log --since="4 hours ago" --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)' --all
    # lg2 = git log --since="4 hours ago" --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)' --all
    # lg = !"git lg1"
    pass

def git_simple(cc, repo):
    count = 0
    current_branch, remote_status = menu.current_status(repo)
    c='checkout master'
    result = lib.gfunc.execute_git_command(repo["path"], c)

    c='log --graph --oneline --decorate -1000'
    result = lib.gfunc.execute_git_command(repo["path"], c)
    lib.cutie.color_print('WHITE','\n----------------------- Git Graph (last 20 branch level event)-----------------------')
    for r in result:
        if count > 20:
            break
        if '*' in r:
            if 'Merge pull request' in r: 
                lib.cutie.color_print('GREEN',string_filter(r))
                count += 1            
            elif '(' in r :
                lib.cutie.color_print('YELLOW', string_filter(r))
                count += 1
            else:
                pass
                # lib.cutie.color_print('MAGENTA', string_filter(r))
                # count += 1                
        else:
            lib.cutie.color_print('WHITE',r)
            count += 1
    lib.cutie.color_print('WHITE','\n----------------------- Git Graph             (end)          -----------------------\n')
    c='checkout ' + current_branch
    result = lib.gfunc.execute_git_command(repo["path"], c)

def string_filter(r):
    f = r'origin/\S*(, |\))'
    r = re.sub(f,'', r)
    return r