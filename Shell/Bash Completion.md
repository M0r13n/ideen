# Bash Completion

Bash completion is a feature that helps users to type their commands faster and easier. This is accomplished by listing possible options (completions), when a user types the `TAB` key after a command.

## Installation
In order to use bash completion the packet `bash-completion` needs to be installed. This can be done via apt:

```
$ sudo apt install bash-completion -y
```

This will also add a new entry to `/etc/bash.bashrc`:
```bash
[ -r /usr/share/bash-completion/bash_completion   ] && . /usr/share/bash-completion/bash_completion
```

## How does it work

The fundamental part is the `complete` command. The command basically takes two arguments:

1. a function that determines, which completion suggestions can be displayed for a given executable
2. a name of a executable that should be completed

If a user types a command and then presses `TAB`, the bash will check if a entry exists for the command. If so, it will call the associated function.

## Examples and Snippets

### Simple wordlist
- pass the `-W` (wordlist) parameter
- pass a string of `space separated` words that are used for completion

```bash
$ complete -W "Foo Bar Faz Boo" <NANME_OF_YOUR_COMMAND>
```

### Delete an entry
All entries can be listed by just typing `complete`. You can delete an entry by using the `-r` parameter.

### Dynamic
- define a function that handles completion in a bash file
- Best practice name it: `_<NAME_OF_COMMAND_TO_CPLETE>_completions`
- inside the function `COMPREPLY` is an array used to store the completions
- `compgen` is builtin command that generates completions and filters them based on the input a user already typed

```bash
$ compgen -W 'foo bar baz'
foo
bar
baz

$ compgen -W 'foo bar baz' f
foo

$ compgen -W 'foo bar baz' ba
bar
baz
```

**NOTE** when using `compgen`: the `-W` option takes a list of comp-words, but it must be in the form of a single shell-word with the comp-words separated by spaces. So `compgen -W "${commands[@]}"` will **NOT** work. Use `compgen -W "${commands[*]}"` instead. See [[Bash Completion]].


### Example for make.sh

```bash
#!/usr/bin/env bash

declare -a commands=(
    "install"
    "configure"
    "build"
    "deploy"
    "get_deps"
    "info"
    "clean"
)

_make_sh_completions() {
    COMPREPLY=($(compgen -W "${commands[*]}" "${COMP_WORDS[-1]}"))
}

complete -F _make_sh_completions "make.sh"
```