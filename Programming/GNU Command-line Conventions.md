There are some conventions on how to interpret command-line arguments. Generally, there are two categories of arguments:

- **options**: also called flags change the behavior of a program
- **arguments**: provide inputs for the program

Options should come in two forms:
- **short options** are single characters and are faster to type (`-o output.txt`)
- **long options** are multiple characters and are more verbose (`--output output.txt`)

Options should precede arguments: `ls -s /`

The GNU Coding Standards provide a list of common names for common options. The list can be viewed from the terminal: ` info "(standards)User Interfaces"`.
