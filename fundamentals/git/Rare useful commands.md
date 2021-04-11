# Rare (but useful) Git commands


### Keep a file in a git repo, but dont track it's changes

##### Dont track changes
 <del>`git update-index --assume-unchanged FILE_NAME`</del>

Do not use, because `--assume-unchanged` assumes that a developer **shouldn’t** change a file. This flag is meant for **improving performance** for not-changing folders like SDKs.

Better:

`git update-index --skip-worktree FILE_NAME`

Track changes again

<del>`git update-index --no-assume-unchanged FILE_NAME`</del>

`git update-index --no-skip-worktree FILENAME`