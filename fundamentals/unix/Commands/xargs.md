# `xargs`

`xargs` takes a command as an argument an runs it against a text stream from stdin.  A very useful GNU extension is `xargs -P`, which starts processes in parallel.



## Examples

Echo all lines in a file line by line and word by word (`xargs` splits by space by default):
`cat input.txt | xargs echo`

Echo at most `N` words per line (will split longer lines into multiple lines):
`cat input.txt | xargs -n 1 -- echo`

Read a file directly:
`xargs -a input.txt -- echo`

Split input stream by different delimiter:
`xargs -a  input.txt -d $'\n' -- printf "%s\n"`

Run processes in parallel (`args` starts a few processes as possible) with the `-P` parameter:
`xargs -a ./input.txt -n 1 -P 5-- curl -L`


Combine with other builtins:

```bash
$ find ... | grep ... | xargs ...
$ find ... | head | xargs ...
```