There are four (4) main object types in Git.

## Blob
- contents of files are stored as **blobs**
- **only** the content of a file is stored 
- the files itself is not part of the blob
- same applies to file permissions, etc
- this means, that **different** files, with the **same** content, also point to the **same** blob
- **blobs** are expanded during checkout and turned back into files
- the file content is hashed into a 40 character SHA sum
- the compressed file contents (via `zlib`) can then be found inside:
	* .git/<FIRST_2_CHARS_OF_SHA_SUM>/<LAST_38_CHARS_OF_SHA_SUM>


## Tree
- how Git tracks directories
- leafs are blobs and non-leaf vertices are again (sub)-trees
- every tree object consists of a simple text file that lists for each entry:	
  * mode
  * type
  * name
  * sha sum
  * e.g.
  * `100644 blob a906cb README`
  * `100644 blob a874b7 Rakefile`



## Commit
- used to keep track of the history of Git
- each commit points to a tree and keeps information about:
  * author
  * committer
  * message
  * parent commits






## Tag
- permanent shorthand for a given commit
- contains: `object`, `type`, `tag`, `tagger` and `message`