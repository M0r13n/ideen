# AppImages

**AppImages can be downloaded and run without installation or the need for root rights.**

## Summary

- simple format (the whole application is self contained in a single file)
- binary-compatible with many systems
- distribution agnostic
- an AppImage is decompressed on the fly and never fully decompressed to the drive
- readonly applications
- rootless usage and installation
- should be installed to `${HOME}/Applications/` or  `${HOME}/bin/` (see [[Linux Directory Structure]])
- [FAQ](https://docs.appimage.org/user-guide/faq.html#question-where-do-i-store-my-appimages)


## Installation of a *.appimage

```bash
chmod a+x program.AppImage
```

