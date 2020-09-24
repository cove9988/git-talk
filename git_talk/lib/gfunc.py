import subprocess
import os
import git_talk.lib.cutie as cutie
import git_talk.lib.bcolors as bcolors

bcolors = bcolors.bcolors()

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
            cmd = '-CMD-{0}->'.format(n) + ' '.join(c) 
            cutie.color_print('YELLOW', cmd)
        if os.name != 'nt':
            c = ' '.join(c)
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
