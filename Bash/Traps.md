# Trap command

## Syntax

`trap [action] [signals]`


## Options

- list all signals: `trap -l`


## Example

### Multiple signals
`trap 'echo Trap command executed' 1 3 9`

### Cleanup
```
function cleanup()
{
    \# ...
}

trap cleanup EXIT
```

### Capture ^+C


```bash
ctrlc\_count\=0

function no\_ctrlc()
{
    let ctrlc\_count++
    echo
    if \[\[ $ctrlc\_count \== 1 \]\]; then
        echo "Stop that."
    elif \[\[ $ctrlc\_count \== 2 \]\]; then
        echo "Once more and I quit."
    else
        echo "That's it.  I quit."
        exit
    fi
}

trap no_ctrlc SIGINT

while true
do
    echo Sleeping
    sleep 10
done
```

### Cleanup

```bash
kill_all_subprocesses() {
  local i=""

  for i in $(jobs -p); do
    kill "$i"
    wait "$i" &> /dev/null
  done
}

# If the current process is ended,
# also end all its subprocesses.

set_trap "EXIT" "kill_all_subprocesses"

```