# Common public key certificate formats & conversion

- every SSL certificate is a **[x.509 certificate](https://en.wikipedia.org/wiki/X.509)**
- private keys, public keys, certificate signing requests, etc can be stored in these formats


- **DER**
	- binary
	- Distinguished Encoding Rules
	- only really used on Windows systems
	- typical file extensions: 
			- `.der`
			- `.cer`
- **PEM**
	- ASCII encoded
	- Privacy-Enhanced Email
	- today is has nothing to with mails anymore
	- Base64 encoded DER file
	- most popular as it is plain ASCII and can be viewed in any text editor (nano, Notepad++)
	- can contain a single certificate or **all intermediate certificates**:
		- `-----BEGIN CERTIFICATE REQUEST----- and -----END CERTIFICATE REQUEST----`
		- `-----BEGIN RSA PRIVATE KEY----- and -----END RSA PRIVATE KEY-----`
		- `-----BEGIN CERTIFICATE----- and -----END CERTIFICATE-----`
		- `-----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY-----`
	- can also contain the **private key**(!)
	- typical file extensions:
		- `.pem`
		- `.crt`
		- `.cer`
		- `.key`
- **PKCS#7**
	- ASCII encoded
	- Public Key Cryptography Standards
	- typical file extensions:
		- `.p7b`
		- `.p7c`
-  **PKCS#12**
	- binary
	- the same as PKCS but with password protection
	- typical file extensions:
		- `.pfx

## Convert Formats

###### Convert X.509 to PEM
- `openssl x509 -in <IN>.cer -outform PEM -out <OUT>.pem`

###### **Convert DER to PEM** (Binary encoding to Base64 ASCII)
- `openssl x509 -inform der -in <IN>.der -out <OUT>.pem`

###### **Convert PEM to DER** (Base65 ASCII to binary encoding)
- `openssl x509 -inform der -in <IN>.der -out <OUT>.pem`

###### **Convert PEM to PKCS#7** (the .p7b file does not include the private key)
- `openssl crl2pkcs7 -nocrl -certfile <IN>.pem -out <OUT>.p7b -certfile CACert.cer`

###### **Convert PKCS#7 to PEM**
- `openssl pkcs7 -print_certs -in <IN>.p7b -out <OUT>.pem`

###### **Convert PKCS#12 to PEM** (PKCS#12 file is password-protected)
- `openssl pkcs12 -in <IN>.pfx -out <OUT>.pem`
