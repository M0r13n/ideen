A good comparison is given by [[the AppImages authors]] [here](https://github.com/AppImage/AppImageKit/wiki/Similar-projects#comparison).

Flatpak und Snap promise to solve dependency problems by **bundling software with all of its (runtime) requirements**. Developers can therefore distribute their software more easily across many distributions, without having to build dozens of packages for each distribution.

Flatpak and Snap packages **contain nearly all of their runtime dependencies** - unlike system packages like [[Creating Debian Package|deb]] or rpm. This includes runtime libraries, interpreters and data. Flatpak can only be used for Desktop applications while **Snap can also be used for server applications** and command line applications. In fact, Snap originates from Ubuntu Core where every application is a Snap package. Snaps are installed system wide while Flatpaks can be installed in the home directory **without requiring root permissions**.

Both Flatpak and Snap provide a basic set of functionalities. Flatpak provides a runtime that bundles Gnome and it's dependencies (Glibc, OpenSSL, GTK+ …). Such a basic set of functionalities also exists in Snap: Ubuntu Core. This snap provides the C-lib and OpenSSL. A snap offers only in combination with the OS snap everything that the contained application needs to run under modern distributions. This applies similarly to Flatpak and Flatpak Runtime, although Flatpaks that work without Runtime are also possible.

### Disadvantages

- multiple versions of the same dependencies
	- each snap comes with its own copy of all of its dependencies
	- waste of space
	- potential security issues
		- each package must be updates by its maintainer individually

### Inner workings

Both Snap and Flatpaks belong into their own directories to prevent conflicts with system packages. The snap [file format](https://en.wikipedia.org/wiki/File_format "File format") is a single compressed [filesystem](https://en.wikipedia.org/wiki/File_system "File system") using the [SquashFS](https://en.wikipedia.org/wiki/Squashfs "Squashfs") format with the extension `.snap`. This filesystem contains the application, libraries it depends on, and declarative metadata. After installation, the snap is mounted by the host operating system and decompressed on the fly when the files are used ([[Loopback file]]). Although this has the advantage that snaps use less disk space, it also means some large applications start more slowly ([Canonical felt compelled to write a dedicated blog post about the improvement of the Firefox startup time](https://snapcraft.io/blog/improving-firefox-snap-performance-part-3)). They are written to **/var/lib/snapd/snaps/** and mounted under **/snaps/**. Flatpaks are located in **/var/lib/flatpak/** (system wide installation) or in **~/.local/share/flatpak** (user wide installation).

### Security

Applications in a Snap run in a container with limited access to the host system. Using _Interfaces_, users can give an application mediated access to additional features of the host such as recording audio, accessing USB devices and recording video.

The Snap sandbox also supports sharing data and Unix sockets between Snaps. This is often used to share common libraries and application frameworks between Snaps to reduce the size of Snaps by avoiding duplication.

The Snap sandbox heavily relies on the [[AppArmor]] Linux Security Module from the upstream Linux kernel. Because only one "major" Linux Security Module (LSM) can be active at the same time the Snap sandbox is much less secure when another major LSM is enabled. As a result, on distributions such as Fedora which enable SELinunx by default, the Snap sandbox is heavily degraded.

Unlike Snap Flatpak uses Namespaces and chroot to ensure that the program is executed in its own isolated environment.




