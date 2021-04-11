# Case Statement


```bash
case EXPRESSION in

  PATTERN_1)    			# Every pattern is terminated by )
    STATEMENTS				# Each pattern has associated commands
    ;;						# Every clase is terminated by ;;

  PATTERN_2 | PATTERN_3) 	# Join multiple patterns with |
    STATEMENTS
    ;;
							# <---------
  PATTERN_N)				#  |
    STATEMENTS				#  | This is a clause
    ;;						#  |
							# <-----------
							
  *)						# * matches every pattern and thus
    STATEMENTS              # can be used as a default pattern
    ;;
esac

# Returns 0 if not pattern matched.
# Returns the exit status of the executed commands otherwise
```


## Example

```bash

if [ -z "$1" ]; then
		echo "Please provide a valid filename as a single argument."
		return 1
fi

local filepath="$( realpath -- "$1" )"
local extension="${filepath##*.}"

if [ ! -f "$filepath" ]; then
		echo "$filepath is not a file"
		return 1
fi

case "$extension" in

"deb")
		echo "Debian package provided. Using \"apt install ...\""
		sudo apt install "$filepath"
		;;

"snap")
		echo "Snap package provided. Using \"snap install ...\""
		snap install "$filepath"
		;;

*)
		echo  "Unknown filetype: $extension"
		;;
esac

```