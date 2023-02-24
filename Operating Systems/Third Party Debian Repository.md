According to the [official documentation](https://wiki.debian.org/DebianRepository/UseThirdParty):

- Repositories MUST be signed with an OpenPGP certificate
- a binary export (`gpg --export`)  should be available at **/deriv-archive-keyring.pgp
- an ASCII-Armored (`gpg --export --armor`) MAY be available under **deriv-archive-keyring.asc**
- certificates SHOULD be served over HTTPS
- certificates MAY also be served on additional key servers
- certificates should only be writable by root
- certificate MUST NOT be placed in **/etc/apt/trusted.gpg.d** or loaded by `apt-key add`
- apt/dpkg SHOULD place additional certs into **/usr/share/keyrings**
- locally managed certs SHOULD be downloaded into **/etc/apt/keyrings**
	- */etc/apt/keyrings may not exist by default*
- sources SHOULD have the signed-by option set:
	- `deb [signed-by=/etc/apt/keyrings/deriv-archive-keyring.pgp] https://deriv.example.net/debian/ stable main`
- import a repo's key from a keyserver:
	- ``gpg --no-default-keyring --keyring <output-file-name>.gpg --keyserver <some.keyserver.uri> --recv-keys <fingerprint>``

>The reason we point to a file instead of a fingerprint is that the latter forces the user to add the certificate to the global [SecureApt](https://wiki.debian.org/SecureApt) trust anchor in **/etc/apt/trusted.gpg.d**, which would cause the system to accept signatures from the third-party keyholder on all other repositories configured on the system that _don't_ have a **signed-by** option (including the official Debian repositories)

> Serving the repository under HTTPS is OPTIONAL, as it may make running a round-robin network of untrusted mirrors more difficult, and the trust chain provided by [SecureApt](https://wiki.debian.org/SecureApt) should suffice

## Key id

For any given key:

```txt
pub   rsa4096 2012-05-11 [SC]  
     8439 38DF 228D 22F7 B374  2BC0 D94A A3F0 EFE2 1092  
uid           [ unknown] Ubuntu CD Image Automatic Signing Key (2012) <cdimage@ubuntu.com>
```

the key id are the last 8 characters of the public fingerprint:

`EFE21092`

## Ansible

```yaml
- name: Add apt repository key.
  become: true
  ansible.builtin.get_url:
    url: "{{ repo_key_url }}"
    dest: "/etc/apt/keyrings/{{ repo_key_file }}"
    mode: '0644'
    force: true

- name: Add apt repository.
  ansible.builtin.apt_repository:
    repo: "deb [signed-by=/etc/apt/keyrings/{{ repo_key_file }}]  {{ repo_url }}"
    state: present
    update_cache: true
```