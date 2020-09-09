import os
from datetime import date
from collections import defaultdict

import git_talk.lib as lib
import git_talk.menu as menu

# Dict for settings the display name of the categories
# For example, features are tag with `feat:` in the commits
# but I want to display Features in the changelog.
# Also, any category not in this dict are ignored, in this way
# you can control the categories you want to display.
CATEGORIES = {
    'feat': 'Feature',
    'fix': 'Bug Fixes'
}


def get_commits(cc, repo, ver):
    # Run cmd
    command = [['git', 'log', '--format=%B%H----DELIMITER----', f'{ver}..HEAD']]
    stdout, error = lib.gfunc.subprocess_cmd(repo['path'],command)
    # Split output and filter.
    outputs = filter(None, (stdout.decode()).split('----DELIMITER----\n'))
    commits = [{'sha': sha, 'message': msg}
               for msg, sha in map(lambda x: x.split('\n'), outputs)]

    commits_dict = defaultdict(list)

    for commit in commits:
        category, message = commit['message'].split(':', 1)
        commits_dict[category].append(message.strip())

    return commits_dict


def get_current_version(repo):
    return repo["version"]


def bumper_changelog(cc,repo):
    current_date = date.today().isoformat()
    current_version = get_current_version(repo)
    changelog = f"# {current_version} ({current_date})\n\n"

    commits = get_commits(cc, repo, current_version)
    for category, messages in commits.items():
        if category in CATEGORIES:
            changelog += f'## {CATEGORIES[category]}\n\n'
            for message in messages:
                changelog += f'- {message}\n'
            changelog += '\n'
    changlog_file = os.path.join(repo["path"],'changelog.md')
    print(changelog)
    # if os.path.exists(changlog_file):
    #     with open(changlog_file, 'r') as f:
    #         data = f.read()
    #     with open(changlog_file, 'w') as f:
    #         f.write(changelog + '\n\n' + data)
    # else:
    #     with open(changlog_file, 'w') as f:
    #         f.write(changelog)
