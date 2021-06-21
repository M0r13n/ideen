# The problem with git

I can set

	- `git config user.name`
	- `git config user.email`

to whatever string I want. Therefore I would make a commit as someone else. It is also possible to tamper with commits of user users.



## Setting up Git to sign commits

1. Install GPG: `sudo apt install gpg`
2. Create a fresh key pair: `gpg --full-gen-key`
	* on Windows: `gpg --gen-key`
3. Supply all needed information (make sure to use a verified mail)
4. List keys: `gpg --list-secret-keys --keyid-format LONG <your_email>`
	```
	sec   rsa4096/268100ABB6E5776A 2021-05-02 [SC]
		  418D9DE0553A43276B18011D268100ABB6E5776A
	uid                 [ultimate] Leon Morten Richter <me@leonmortenrichter.de>
	ssb   rsa4096/383B5313D10E11E5 2021-05-02 [E]
	```
5. Export public key: `gpg --armor --export 268100ABB6E5776A`
6. Tell git which key use to sign commits: `git config --global user.signingkey <KEY_ID>`
7. Tell git to sign every commits: `git config --global commit.gpgsign true`

### Additional configuration on Linux
1. Create `~/.gnupg/gpg.con`
2. Add the line: `use-agent` (enables `gpg-agent`)




## Add multiple mail addresses

You can add multiple email addresses by editing the key:

```sh
gpg --edit-key <KEY_ID>
```

In the GPG prompt, then type:

```sh
gpgp> adduid
```

Again, type the real name and the email address you want to add.

Then, still in the GPG prompt, update the trust for the new identity:

```sh
# Use the number of the UID of the identity
gnupg> uid 2
gnupg> trust
# Type "5" (for "I trust ultimately")
```

Lastly, save and exit with:

```sh
gnupg> save
```


### Error: `gpg: signing failed: Inappropriate ioctl for device`

By default, Ubuntu asks for passphrases using a GUI dialog. This does not work, if operating headless (e.g. via SSH). In order to solve this, I can tell `gpg` to use a [[TTY | terminal]] (`tty`).

```bash

# Firstly, install pinentry-tty
$ sudo apt install pinentry-tty

# Configure the tty
$ sudo update-alternatives --config pinentry
```

Alternatively, I can add the following to my `.bashrc`:

```bash
# use a tty for gpg
# solves error: "gpg: signing failed: Inappropriate ioctl for device"
GPG_TTY=$(tty)
export GPG_TTY
```