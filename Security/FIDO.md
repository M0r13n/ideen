The FIDO protocol is based on **public key cryptography**. During registration the client creates a keypair and registers the public key on the server. The client maintains such a keypair for every service. The client authenticates itself by proving possession of the private key by signing a challenge.

It is partially based on [[WebAuthn]].

## Benefits

- immune to phishing
- makes 2FA redundant

## Disadvantages

- access to the private key grants permission to login
	- password can theoretically remain inside the users brain
	- if an attacker or state has access to the users device
	- and also knows the pass-code
	- then he has access to ALL passphrases