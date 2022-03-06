# YubiKey & SSH

See also [[fundamentals/protocols/ssh/Fundamentals]].

Verify, that Ubuntu-18+ and OpenSSH_8.2 is installed:

`lsb_release -d && ssh -V`

My Yubikey 4 only supports `ecdsa-sk` keypairs, because it's firmware version is `4.37`. The firmware can be seen with:

`lsusb -v 2>/dev/null | grep -A2 Yubico | grep "bcdDevice" | awk '{print $2}'`

A key can be generated with the following command:

`ssh-keygen -t ecdsa-sk -C "some comment about the key (include a note about the yubikey is recommended)"`

## What happens here?

`ssh-keygen -t ecdsa-sk` generates an Elliptic Curve Digital Signature Algorithm (**ECDSA**) keypair (public and private) and places these keys into your `~/.ssh` folder. **ECDSA** is an improved system compared to **RSA**. The `-sk` suffix stand fors *security-key* and is a special extension for security keys like the Yubikey. The private key is protected through by secret that is stored on the yubikey. This means you have to explicitly authorize a new SSH session by tapping the YubiKey.

## Important

On newer keys with Firmware version `5.13` and above the `ed25519-sk` is preferred over `ecdsa-sk`.