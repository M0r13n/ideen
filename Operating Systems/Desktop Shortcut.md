# Desktop Shortcuts Ubuntu 22.04

Create a shortcut:

```bash
nano ~/Desktop/shortcut.desktop
```

with the following contents:

```txt
[Desktop Entry]
Name=Some Name
Comment=Do something
Exec=/path/to/some/executable
Icon=~/.local/share/icons/icon.png
Terminal=true
Type=Application
Categories=Utility;
```

make it executable:

```bash
chmod +x ~/Desktop/shortcut.desktop
gio set ~/Desktop/shortcut.desktop metadata::trusted true
```
