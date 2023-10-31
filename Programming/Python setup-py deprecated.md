# TL;DR: setuptools.py should not be invoked directly

- `setuptools` itself remains fully supported
- `setup.py` can still be used to configure the build
- the `setup.py` file just **MUST NOT be invoked directly**
- [some background information](https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html)
- [sample project](https://github.com/pypa/sampleproject/tree/main)

## Migration
| setup.py command  |	New command |
| --------------------------------------- | ------------------------------------------------------------ |
| `setup.py sdist` `setup.py bdist_wheel` | `python -m build` (with [`build`](https://pypa-build.readthedocs.io/en/stable/)) |
| `setup.py test`                         | `pytest` (usually via [`tox`](https://tox.wiki/en/latest/) or [`nox`](https://nox.thea.codes/en/stable/index.html)) |
| `setup.py install`                      | `pip install`                                                |
| `setup.py develop`                      | `pip install -e`                                             |
| `setup.py upload`                       | `twine upload` (with [`twine`](https://twine.readthedocs.io/en/latest/)) |
| `setup.py check`                        | `twine check` (this doesn't do all the same checks but it's a start) |
| Custom commands                         | [`tox`](https://tox.wiki/en/latest/) and [`nox`](https://nox.thea.codes/en/stable/index.html) environments. |

## Single-sourcing the package version

- [docs](https://packaging.python.org/en/latest/guides/single-sourcing-package-version/#single-sourcing-the-package-version)

```toml
[project]
name = "package"
dynamic = ["version"]

[tool.setuptools.dynamic]
version = {attr = "package.__version__"}
```

