# git-talk

git-talk CLI is a dialog sytle commandline git tool, which help you handle most your daily git chore without any git comand typing.
1. It manages mulitiply git reporisities in one place. reduces context switching and helps you focus.
2. git-talk uses git work flow. 
        All the task branch is created from branch dev.
        Use tag based release in master with auto build change log (changelog.md)
        All commit with pre-build category: **New Features,Fixes,Performance improvements,Refactorings,Docs,Others** 

## Add New Repository:
1. Have remote repo url
2. Create repo local with a few configuration
3. Work flow requires only work on task/hotfix branches, you can not commit directly to master and dev branches. 
![Create New REpository](./git_talk/doc/createnewrepo.gif)

## Swith to a different repository (project)
1. You can manage multiply repositories in one place without context switch.  
![Switch](./git_talk/doc/switchrepo.gif) 

## Commit your changes
1. Commit changes at task branch
2. Change Type Defined.
![Switch](./git_talk/doc/commit.gif) 

## Create a PR
1. Pick a completed task branch
2. Create a PR to dev branch
![Switch](./git_talk/doc/pr.gif) 

## Create a Release Tag and Change Log
1. Once PR reviewed and merged
2. Create a release tag and the changelog will auto generated as well.

![Switch](./git_talk/doc/tag.gif) 
![Switch](./git_talk/doc/tag_web.gif) 

## Rebase
1. Rebase from master to dev
2. re-sync all branches from remote and local.

![Switch](./git_talk/doc/rebase.gif) 

## Branch
1. switch branch, create a new task branch
2. Remove merged or unused branch from both local and remote

![Switch](./git_talk/doc/branch.gif) 

## Graph
1. display latest 20 activaties at branch level

![Switch](./git_talk/doc/graph.gif) 


Many Thanks to:

https://github.com/Kamik423/cutie
https://github.com/Michael-F-Bryan/auto-changelog