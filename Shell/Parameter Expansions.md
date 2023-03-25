# Bash Parameter Expansion

See https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html

## Substitution
- Remove suffix: `${VAR%suffix}` (removes  the shortest matching pattern of `suffix` )
- Remove suffix: `${VAR%%suffix}` (removes  the longest matching pattern of `suffix` )
- Remove Prefix `${VAR#prefix}` ( results the shortest matching pattern of `prefix`)
- Remove Prefix `${VAR##prefix}` ( results the longest matching pattern of `prefix`)
- Replace first match `${var/old/new}`
- Replace all matches `${var/old/new}`
- Replace suffix `${FOO/%from/to}`
- Replace Prefix `${FOO/#from/to`
- Length: `${#var}`

```bash
filename="main.cpp.o"

echo ${filename%.*}				#=> main.cpp 
echo ${filename%%.*}			#=> main

echo ${filename#*.}     		#=> cpp.o
echo ${filename##*.}    		#=> o


echo ${filename/.o/.foo}		#=> main.cpp.foo

echo ${#filename}				#=> 11
```


## Defaults

- `${FOO:-val}` => If FOO is unset or null, the expansion of val is substituted. Otherwise, the value of FOO is substituted.
- `${FOO:=val}` => If FOO is unset or null, the expansion of val is assigned to parameter.
- `${FOO:+val}` => If FOO is null or unset, nothing is substituted, otherwise the expansion of word is substituted.
- `${FOO:?message}` => Show error message + Exit if FOO is unset or null


```bash
echo ${FOO}				#=> Nothing
echo ${FOO:-bar}		#=> bar
echo ${FOO}				#=> still nothing

echo ${FOO:=bar} 		#=> bar
echo ${FOO}				#=> bar (bar is now assigned to FOO)

echo ${FOO:+foo}		#=> foo, because FOO is set
echo ${BAR:+foo}		#=> Nothing, because BAR is unset
```


## Substring / Splitting

- `${FOO:offset:len}` => Get everything from `offset` to `len`


```bash
abc="abcdefghijk"

echo ${abc:5}			#=> fghijk

echo ${abc:0:3}			#=> abc
echo ${abc:3:3}			#=> def

arr=(1 2 3 4 5 6 7 8 9 10 11 12)

echo ${arr[*]:7}		#=> 8 9 10 11 12
echo ${arr[*]0:7}		#=> 1 2 3 4 5 6 7
```


## Manipulation
- `${parameter^pattern}` => Make first letter that matches pattern lowercase
- `${parameter^^pattern}` => Make all letters that match pattern  lowercase
- `${parameter,pattern}` => Make first letter that matches pattern uppercase
- `${parameter,,pattern}` => Make all letters that match pattern uppercase
- if pattern is omitted `?` is used which matches every character