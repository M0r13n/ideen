Just like a keychain in real life, a keyring is used to <mark>group multiple different keys together so that they are easy to find and carry</mark>. Instead of physical keys, the Linux keyring holds various passwords. By default, the **keyring is locked with a master password** which is often the login password of the account. Every user on your system has its own keyring with (usually) the same password as that of the user account itself. You can use the keyring to manually store passwords in encrypted format. A good documentation is found at [wiki.ubuntuusers.de](https://wiki.ubuntuusers.de/GNOME_Schl%C3%BCsselbund/).

## Confusions

- user keyring:  store application passwords in encrypted format
- apt keyring:  used for verifying downloaded packages
- keychain:  used to reuse [SSH](../Networking/ssh/SSH.md#keychain) keys between logins

## SSH

The OpenSSH agent is a command-line utility provided by the OpenSSH suite, which is a widely used implementation of the [SSH](../Networking/ssh/SSH.md) (Secure Shell) protocol. It is the default SSH agent on most Linux distributions and provides basic functionality for managing SSH keys, including adding and using keys for authentication.

On the other hand, the GNOME Keyring SSH agent is a component of the  GNOME Keyring system, which is a password and key management  infrastructure used in the GNOME desktop environment. The GNOME Keyring  SSH agent integrates with the GNOME Keyring system to store SSH keys  securely, along with other sensitive data such as passwords and  certificates. It provides a more advanced and integrated key management  experience within the GNOME desktop environment.

Similar to the GNOME Keyring, KWallet provides a secure storage  mechanism for sensitive data such as passwords, certificates, and SSH  keys. It aims to centralize the storage of confidential information and  provide a convenient way to access and manage that information within  the KDE Plasma environment.

In summary, while all three agents manage SSH keys, the OpenSSH SSH agent is a standalone utility, whereas the GNOME Keyring SSH agent and KWallet are part of the Desktop system and offer more integrated experiences within the GNOME or KDE desktop environment.
