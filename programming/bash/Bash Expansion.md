# Bash Expansions

## [@] vs [*]

- `"${myarray[@]}"` leads to each element of the array being treated as a **separate** shell word
- `"${myarray[**]}"` leads to a single shell-word with all the elements of the array separated by the first value of `IFS` - usually space


```bash
my_arr=("foo" "bar")

ls "${my_arr[*]}" <=> ls "foo bar"

ls "${my_arr[@]}" <=> ls "foo" "bar"
```