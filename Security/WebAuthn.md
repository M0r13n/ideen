The Web Authentication API (also known as WebAuthn) is a specification written by the W3C and FIDO, with the participation of Google, Mozilla, Microsoft, Yubico, and others. The API allows servers to register and authenticate users using public key cryptography instead of a password.

It allows servers to integrate with the strong authenticators now built into devices, like Windows Hello or Apple’s Touch ID. Instead of a password, a private-public keypair (known as a **credential**) is created for a website. The private key is stored securely on the user’s device; a public key and randomly generated credential ID is sent to the server for storage. The server can then use that public key to prove the user’s identity.

It is part of the [[FIDO framework]].

In WebAuthn, a server must provide data that binds a user to a credential (a private-public keypair); this data includes identifiers for the user and organization (also known as the "relying party"). The website would then use the Web Authentication API to prompt the user to create a new keypair. It is important to note that we need a randomly generated string from the server as a challenge to prevent replay attacks.

Spec: https://w3c.github.io/webauthn/#sctn-usecase-registration

Lab: https://webauthn.io/
