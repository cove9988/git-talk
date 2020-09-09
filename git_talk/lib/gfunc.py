import subprocess
import os
import git_talk.lib.cutie as cutie
import git_talk.lib.bcolors as bcolors

bcolors = bcolors.bcolors()

lbr = 'refs/heads/'
rbr = 'refs/remotes/'
tr = 'refs/tags/'

def execute_git_command(local_path, command):
    p = os.path.join(local_path, '/.git')
    if os.path.isdir(p):
        cutie.color_print('RED','Not a git repository')
        return []
    bash_command = 'git -C ' + str(local_path) + ' ' + command
    # cutie.color_print('YELLOW',bash_command)
    try:
        output = subprocess.run(bash_command.split(), stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        cutie.color_print('RED','Not a git command')
        return []
    else:
        result = output.stdout.decode('utf-8').splitlines()
        return result


def subprocess_cmd(local_path, command, display=True):
    result = []
    wd = os.getcwd()
    os.chdir(local_path)
    error = 0
    #commands = command.split(";")
    for n, c in enumerate(command):
        if display:
            cmd = '-cmd-{0}->'.format(n) + ' '.join(c) 
            cutie.color_print('YELLOW', cmd)
        output = subprocess.Popen(
            c, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = output.communicate()
        out, err = out.decode("utf-8"), err.decode("utf-8")
        if err:
            if 'error:' in err or 'fatal:' in err:
                #if display:
                ee = '-ERR->' + err
                cutie.color_print('RED', ee)
                error = 1
                break
            else:
                if display:
                    cutie.color_print('GREEN', '-INF->' + err)
        if out:
            if display:
                cutie.color_print('GREEN', '-OUT->' + out)
            result.append(out)
    os.chdir(wd)

    return result, error

def read_git_file(local_path, sha1_file):
    return execute_git_command(local_path, 'cat-file -p ' + sha1_file)

def get_git_objects(local_path):
    objects = [line.split() for line in execute_git_command(
        local_path, 'cat-file --batch-check --batch-all-objects')]
    blobs = [obj[0] for obj in objects if obj[1] == 'blob']
    trees = [obj[0] for obj in objects if obj[1] == 'tree']
    commits = [obj[0] for obj in objects if obj[1] == 'commit']
    annotated_tags = [obj[0] for obj in objects if obj[1] == 'tag']
    return blobs, trees, commits, annotated_tags


def get_git_references(local_path):
    references = [line.split()
                  for line in execute_git_command(local_path, 'for-each-ref')]
    local_branches = {ref[2][len(lbr):]: ref[0]
                      for ref in references if ref[2].startswith(lbr)}
    remote_branches = {ref[2][len(rbr):]: ref[0]
                       for ref in references
                       if ref[2].startswith(rbr) and '/HEAD' not in ref[2]}
    tags = {ref[2][len(tr):]: ref[0]
            for ref in references if ref[2].startswith(tr)}
    return local_branches, remote_branches, tags


def get_git_local_head(local_path):
    symbolic_ref = execute_git_command(local_path, 'symbolic-ref HEAD -q')
    if symbolic_ref:
        return symbolic_ref[0][len(lbr):]
    else:
        commit = execute_git_command(local_path, 'rev-parse HEAD')
        return commit[0]


def get_git_remote_heads(local_path):
    lines = execute_git_command(local_path, 'branch -rv --abbrev=0')
    lines_split = [line.split() for line in lines if '/HEAD ' in line]
    remote_heads = {ls[0]: ls[2] for ls in lines_split}
    return remote_heads


def get_git_upstreams(local_path):
    lines = execute_git_command(local_path, 'branch -vv --abbrev=0')
    lines_split = [line[2:].split() for line in lines if '[' in line]
    upstreams = {ls[2][1:-1]: ls[0] for ls in lines_split}
    return upstreams
