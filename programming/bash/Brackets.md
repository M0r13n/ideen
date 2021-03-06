# Bash bracket operators explained

## `[`
This is a shorthand for the `test` command. This makes it possible to use args like `-x` or `-s` to check if files exists, are empty, etc. `[` is essentially an alias for `test` and `]` is the last argument.


## `[[`
Improved version of `[` that is supported by _bash_, _zsh_, _yash_, _busybox_ _sh_.  Most useful feature is wildcard pattern matching for strings. Less portable than `[ ]`

## `(`
Run a command in a subshell.

```bash
# This command is run in a subshell and therefore does not change the parent's shell directory
$ (cd /tmp && sleep 3) && pwd

/home/leon
```

If prefixed with a $, this command is a [[Command Substitution| command substitution]]: Run the command inside the parentheses and return the output of the command to calling command

```bash

$ echo $(cd a && sleep 1 && echo Hello World)
Hello World

```


## `((`
`ksh`, `bash` and `zsh` extension that performs arithmetic:

```bash
leon at DESKTOP-0PQNS09 in /tmp/push
$ foo=42

leon at DESKTOP-0PQNS09 in /tmp/push
$ bar=1337

leon at DESKTOP-0PQNS09 in /tmp/push
$ echo $((foo+2))
44

leon at DESKTOP-0PQNS09 in /tmp/push
$ ((foo+=2))

leon at DESKTOP-0PQNS09 in /tmp/push
$ echo $foo
44

leon at DESKTOP-0PQNS09 in /tmp/push
$ echo ((foo+=bar))
-bash: syntax error near unexpected token `('

leon at DESKTOP-0PQNS09 in /tmp/push
$ echo $((foo+=bar))
1381
```

Also return the result if prefixed with `$`. 