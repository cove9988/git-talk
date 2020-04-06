# git-talk
### It's a easy way to manage your daily git related works in an interactive way. You can manage mulitple repositories in one place by using command line
- 1. clone new repository to you local
- 2. checkout, create, or delete a branch
- 3. commit your works at local and remote
- 4. create PR 
- 5. create, assign and complete an issue (feature) with auto linked branch
- 6. rebase easily

Very good and easy understanding reference here:
https://www.atlassian.com/git/tutorials/making-a-pull-request

Key bindings .

| Key          | Mode   | Description |
| ------------ | ------ | ----------- |
|  Up          | All    | Move selection up |
|  Down        | All    | Move selection down |
|  Page Up     | All    | Move selection up five lines |
|  Page Down   | All    | Move selection down five lines |
|  Space       | All    | Multi selection |
|  Enter       | All    | Confirmation |

## issues
- [ ] git rebase
- [ ] git story (issue)

## Install

#### From GitHub
To install git-talk from GitHub:
1. You first need to install [git]() and check that the dot binary is correctly set in you system's path.  
2. Then run:
    ```
    git clone https://github.com.au/cove9988/git-talk
    ```
3. Finally, inside the newly created git-talk folder, run (with Python 3 and setuptools):
    ```
    python setup.py install
    ```

## Run

#### As a Git plugin
git-talk is a Git plugin that is run from a Git repository with the command:
```
git talk
```


## Functions
### commit your work
    (including git pull, git add/rm, git commit -m, git push)

#### pull
    git pull has two problems:

    * It merges upstream changes by default, when it's really more polite to `rebase
      over them <http://gitready.com/advanced/2009/02/11/pull-with-rebase.html>`__,
      unless your collaborators enjoy a commit graph that looks like bedhead.

    * It only updates the branch you're currently on, which means git push will
      shout at you for being behind on branches you don't particularly care about
      right now.

<pre>
            (remote origin/master)
     a--b--c  
    /       \
 d--         \
    \         \
     e--f--g---h 
              (local master)
</pre>


#### git pull --rebase
the rebase has copied the remote commits A--B--C and appended them to the local origin/master commit history.

<pre>
            (remote origin/master)
     a--b--c  
    /       
 d--         
    \         
     e--f--g--a--b--c 
                    (local master)
</pre>


#### tagging
Tags are ref's that point to specific points in Git history. Tagging is generally used to capture a point in history that is used for a marked version release (i.e. v1.0.1). A tag is like a branch that doesn’t change. Unlike branches, tags, after being created, have no further history of commits. \


### rebase
In our day-to-day git workflow, you have many topic (feature, issue) branches, like so:

<pre>
              i--j--k (branch-2)
             /
         g--h (branch-1)
        /
 a--b--c (master)
        \
         d--e--f (branch-3)
</pre>

When you pull from upstream,

<pre>
              i--j--k (branch-2)
             /
         g--h (branch-1)
        /
 a--b--c--x--y--z (master)
        \
         d--e--f (branch-3)
</pre>

You want to **rebase** all your topic branches on top of the new master:

<pre>
                        i'--j'--k' (branch-2)
                       /
                  g'--h' (branch-1)
                 /
 a--b--c--x--y--z (master)
                 \
                  d'--e'--f' (branch-3)
</pre>

### Create PR
