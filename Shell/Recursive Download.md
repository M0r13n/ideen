# Download files recursively with wget

```bash
wget --recursive --no-parent --no-directories -R "index.html*" -P "${DEST_DIR}" "some-url"
```

- `--no-directories` -> don't create directories locally
- `-R index.html` -> ignore index files
- `P dir` -> save files to this directory