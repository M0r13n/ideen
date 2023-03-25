- images are exchanged via a network to a private or public registry
- content trust **verify both the integrity and the publisher of all the data** received from a registry over any channel -> integrity and authenticity
- based on digital signatures
- signatures are verified on the client side at runtime
- DCT is associated with the tag portion of the image
	- publishers may choose to sign any tag of an image
- currently opt-in for the client
	- `export DOCKER_CONTENT_TRUST=1`
- ensures that images are signed by the appropriate signer, not tampered with and signed recently (freshness)

![Signing keys relationship](https://docs.docker.com/engine/security/trust/images/trust_components.png)

## Flow

1.  The Docker client requests the image from the Docker registry and checks whether the image is signed.
2.  If the image is signed, the Docker client retrieves the signature from the Notary server.
3.  The Docker client verifies the signature using the public key of the signing keypair, which is also stored in the Notary server.
4.  If the signature is valid, the Docker client can be assured that the image is authentic and has not been tampered with.