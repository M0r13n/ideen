# Git hooks summarized
- can be executed before and after events (*pre-commit*, *pre-receive*, *post-commit*, etc)
- built-in feature (no need for third party tools, but good third-party tooling is available)
- `.git/hooks/` folders contains all scripts
- to enable a hook, place a script named like the hook (e.g. `pre-commit`) in `.git/hooks/`
- [Useful variable set in each hook](https://longair.net/blog/2011/04/09/missing-git-hooks-documentation/)
- hooks can be written in any scripting language (`bash`, `ruby`, `python`, `perl`)
- failing hooks can be ignored by passing `--no-verify` to the original git command
- `git hooks --help` can offer some quick reference
- default hooks can be found under `/usr/share/git-core/templates/hooks/`
- hooks for submodules are to be placed here: `.git/modules/<relative path of your submodule>/hooks/`
- it might be preferred to use symlinks to link to files outside the `.git` dir
 
 
 
 ### GitLab hooks
 How to use server hooks in GitLab
 
 #### Per Repository
 
 1. Locate the project repo path (usually `/var/opt/gitlab/git-data/repositories/<group>/<project>.git`)
 2. [TBW](https://docs.gitlab.com/ee/administration/server_hooks.html#create-a-server-hook-for-a-repository)