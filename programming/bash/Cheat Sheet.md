# Best Practices (IMHO) for bash scripts
Always refer to the [bash manual](https://www.gnu.org/software/bash/manual/bash.html#Command-Substitution)

## Options 
### Fail script if command fails
The bare minimum should be to set `set -e`. By doing so scripts will fail as soon, as a command returns with a non-zero status. This is not enabled by default and will most likely hide errors.

Single commands can be suffixed by `|| true` in order to suppress errors.

Also `if`, `while` and `until` are allowed to fail (conditionals).


### Fail script if unset variables are accessed
Additionally it might be useful to exit the script if unset variables are accesses. This can be done via `set -u`.  If an unset variable is then accessed while running the script an error will occur:

```sh
line 123: NOT_SET: unbound variable
```

### Fail pipes
By using `set -o pipefail` a pipeline will only return `0` if all commands succeed (exit with `0`).


## Variables

### Prefer local variables
```bash
func()
{
	local loc_a=42					# Local variables have a local scope
	local lob_b="1337"				# so they are only accessible in the function
	glob_var="i am global"			# Not declared as local and therefore global
}

```

### Global variables should be readonly
```bash
declare -r GLOBAL_READONLY=1337
readonly GLOBAL_B=42


# The following will fail
$ GLOBAL_READONLY=1336
-bash: GLOBAL_READONLY: readonly variable


$ GLOBAL_B=1337
-bash: GLOBAL_B: readonly variable


```

### Wrap vars in brackets `{}`
Prefer to access variables via `${var_a}` instead of `$var_a`.

## Cleanup
If you touch any files, open sockets, etc, you should **always** cleanup your stuff! This is what [[Traps]] can be useful for. They pattern for traps is :

```sh
trap <command> <signals>
```

e.g.

```sh
function cleanup() {  
    rm foo.bar
}

trap cleanup EXIT

```

## Check for missing programs early
If you need external programs (e.g. Python), you should check if the command is available early. This prevents half-run scripts.


## Don't mess with the user environment
Don't modify the environment of the user. If you need Environment Variables, don't export them.

```bash
# BAD
export PATH="$PATH;$HOME/.local/bin"
export NO_PROXY=192.168.178.1

# Better
PATH="$PATH;$HOME/.local/bin"
NO_PROXY=192.168.178.1
```


## Prefer temp files
```bash
# Random filename
mktemp

# Temp fil in script
local -r TMP_FILE="$(mktemp /tmp/XXXXX)"

# Custom directory (X = random char)
mktemp -d -t foo.XXXXXX


```


## Quote everything
Put every variable in double quotes: `""`.


## Find the right shell
Instead of 

```bash
#!/bin/bash
```

you might want to use:

```bash
#!/usr/bin/env bash
```

This will use the `env` command to find the bash executable in the user's PATH.

## Use full parameters names
Especially if using lesser known commands, it might be preferable to use the long parameter notation instead of the short codes:

```bash
# BAD

rm -r -f "/foo/bar"


# BETTER

rm --recursive --force "/foo/bar"

```

## Don't change the current working dir
As soon as your scripts become more complex, this will LEAD to errors.

#### BAD
```bash
cd "some/dir"
...
cd ~

```

#### Better
```bash

# Add a directory to the top of the directory stack
pushd "some/dir"

# Do something i some/dir
...

# Remove the first directory from stack
popd

```

```bash
pwd
(
    cd "a"
    ls
    pwd
)
pwd
```

## Multiline text

```bash
cat << 'MSG'
usage $0 [OPTIONS]... [ARGUMENTS]...

More text...

MSG
```

## Move complex tests into functions

```bash

help_wanted()
{
	[ "$#" -ge "1" ] && [ "$1" = "-h" ] || [  "$1" = "--help" ]
}

if help_wanted "$@"; then
	echo "Some usage text here..."
	exit 0
fi
```


# Template

```bash
# Get the bash executable from PATH
#!/usr/bin/env bash


# Fail on error and fail early
set -Eeuo pipefail

trap cleanup SIGINT SIGTERM ERR EXIT

readonly SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)

usage() {
  cat <<EOF
Usage: $(basename "${BASH_SOURCE[0]}") [-h] [-v] [-f] -p param_value arg1 [arg2...]
Script description here.
Available options:
-h, --help      Print this help and exit
-v, --verbose   Print script debug info
-f, --flag      Some flag description
-p, --param     Some param description
EOF
  exit
}

cleanup() {
  trap - SIGINT SIGTERM ERR EXIT
  # script cleanup here
}

setup_colors() {
  if [[ -t 2 ]] && [[ -z "${NO_COLOR-}" ]] && [[ "${TERM-}" != "dumb" ]]; then
    NOFORMAT='\033[0m' RED='\033[0;31m' GREEN='\033[0;32m' ORANGE='\033[0;33m' BLUE='\033[0;34m' PURPLE='\033[0;35m' CYAN='\033[0;36m' YELLOW='\033[1;33m'
  else
    NOFORMAT='' RED='' GREEN='' ORANGE='' BLUE='' PURPLE='' CYAN='' YELLOW=''
  fi
}

msg() {
  echo >&2 -e "${1-}"
}

die() {
  local msg=$1
  local code=${2-1} # default exit status 1
  msg "$msg"
  exit "$code"
}

parse_params() {
  # default values of variables set from params
  flag=0
  param=''

  while :; do
    case "${1-}" in
    -h | --help) usage ;;
    -v | --verbose) set -x ;;
    --no-color) NO_COLOR=1 ;;
    -f | --flag) flag=1 ;; # example flag
    -p | --param) # example named parameter
      param="${2-}"
      shift
      ;;
    -?*) die "Unknown option: $1" ;;
    *) break ;;
    esac
    shift
  done

  args=("$@")

  # check required params and arguments
  [[ -z "${param-}" ]] && die "Missing required parameter: param"
  [[ ${#args[@]} -eq 0 ]] && die "Missing script arguments"

  return 0
}

parse_params "$@"
setup_colors

# script logic here

msg "${RED}Read parameters:${NOFORMAT}"
msg "- flag: ${flag}"
msg "- param: ${param}"
msg "- arguments: ${args[*]-}"
```