# Editable installs



- pip and setuptools support **editable installs**
- also known as **“development installation”**
-  Advantage: ==re-installations are only required if the meta data changes==
- non Python code (e.g. C/C++) still needs to re-build
- `pip install --editable .`
- [pip documentation](https://pip.pypa.io/en/stable/topics/local-project-installs/)
- [setuptools documentation](https://setuptools.pypa.io/en/latest/userguide/development_mode.html)

## Limitations

- The *editable* term is used to refer only to Python modules inside the package directories. Non-Python files, external (data) files, executable script files, binary extensions, headers and metadata may be exposed as a *snapshot* of the version they were at the moment of the installation.
- Adding new dependencies, entry-points or changing your project’s metadata require a fresh “editable” re-installation.

## How

An “editable installation” works very similarly to a regular install with `pip install .`, except that it only installs your package dependencies, metadata and wrappers for [console and GUI scripts](https://setuptools.pypa.io/en/latest/userguide/entry_point.html#console-scripts). Under the hood, setuptools will try to create a special [`.pth file`](https://docs.python.org/3/library/site.html#module-site) in the target directory (usually `site-packages`) that extends the `PYTHONPATH` or install a custom [import hook](https://docs.python.org/3/reference/import.html).

Practically, this may look like this:

- `pip install -e .`
  - will create a **<package>.egg-link** in site-packages
    - behaves like a text based symlink
    - first line defines the source
    - second line defines the destination
  - thus the package is in the PYTHONPATH

