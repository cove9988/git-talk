#!/bin/bash

#https://github.com/cove9988/git-rebase-all/blob/master/git-rebase-all

USAGE='<new-upstream> <root>'
OPTIONS_KEEPDASHDASH=
OPTIONS_SPEC="\
git rebase-all <new-upstream> <root>
git rebase-all --continue | --abort | --skip
--
 Actions:
continue!       continue
abort!          abort and check out the original branch
skip!           skip current patch and continue
"

. "$(git --exec-path)/git-sh-setup"
require_work_tree_exists
cd_to_toplevel

total_argc=$#
while test $# != 0
do
  case "$1" in
  --continue|--skip|--abort)
    test $total_argc -eq 2 || usage
    action=${1##--}
    ;;
  --onto)
    test 2 -le "$#" || usage
    onto="$2"
    shift
    ;;
  --)
    shift
    break
    ;;
  esac
  shift
done
test $# -eq 2 || [ x$action != x ] || usage

if [ $# -eq 2 ]; then
  [ x$action != x ] && usage
  # Do setup
  new_upstream=$1
  root=$2

  # Fetch all the branches that contain the root of the subtree
  branches=$(git for-each-ref --contains $root --no-merged $new_upstream --format='%(refname:strip=2)' refs/heads/)

  echo rebasing $branches onto $new_upstream

  # Use the tree from the common ancestor of all the branches. It probably
  # doesn't matter what tree we use, but the merge-base is a) conveniently
  # accessible and b) probably the most sensible thing. Conceptually, this
  # equates to committing an octomerge that undoes everything the topic branches
  # did, which is a well-defined operation.
  merge_base=$(git merge-base $branches)
  tree=$(git cat-file commit $merge_base | head -n1 | cut -c6-)

  # Create the octomerge: a temporary commit that has all the topic branches as
  # parents.
  octomerge=$(echo 'merging' $branches |
    git commit-tree $tree -p `echo $branches | sed -e's/ / -p /g'`)
  git update-ref refs/hidden/octomerge $octomerge || die "couldn't branch"

  # The money shot: rebase the octomerge onto the new upstream.
  git rebase --preserve-merges $root refs/hidden/octomerge --onto $new_upstream ||
    exit $? # if the rebase drops to shell, stop here.
else
  [ x$action = x ] && usage
  # Pass the action through to git-rebase.
  git rebase --$action ||
    exit $? # if it drops to shell again, stop again.
  branches=`git log --format=%s refs/hidden/octomerge -1`
  branches=${branches#merging }
fi

# Move all the old branches to point to the rebased commits.
# The parents of the octomerge remain in the same order through the rebase.
branches_list=($branches)
new_commit_list=(`git rev-parse HEAD^@`)
for index in ${!branches_list[@]}; do
  branch=${branches_list[$index]}
  echo "moving $branch (was $(git rev-parse --short $branch))"
  git branch -f $branch ${new_commit_list[$index]}
done

# and clean up.
git checkout -q ${branches_list[0]}
git update-ref -d refs/hidden/octomerge