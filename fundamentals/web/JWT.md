# JSON Web  Token

A JWT is a stateless token, because is solves the problem of remembering the state on the server side. Instead, the token itself contains the actual user info. So the server save at least a single database request.

## Structure

Signed JWTs have a header, body, and signature.
Each part is separated by a dot (**.**).

```txt
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzY290Y2guaW8iLCJleHAiOjEzMDA4MTkzODAsIm5hbWUiOiJDaHJpcyBTZXZpbGxlamEiLCJhZG1pbiI6dHJ1ZX0.03f329983b86f7d9a9f5fef85305880101d5e302afafa20154d094b229f75773
```

- Header: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
- Payload/Body: eyJpc3MiOiJzY290Y2guaW8iLCJleHAiOjEzMDA4MTkzODAsIm5hbWUiOiJDaHJpcyBTZXZpbGxlamEiLCJhZG1pbiI6dHJ1ZX0
- Sig: 03f329983b86f7d9a9f5fef85305880101d5e302afafa20154d094b229f75773

The header and payload can be decoded by anyone.
Therefore, the data can be used by the server and the client.
Both parts are BASE64 encoded:

```bash
$ echo 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' |base64 -d
{"alg":"HS256","typ":"JWT"}
echo 'eyJpc3MiOiJzY290Y2guaW8iLCJleHAiOjEzMDA4MTkzODAsIm5hbWUiOiJDaHJpcyBTZXZpbGxlamEiLCJhZG1pbiI6dHJ1ZX0'|base64 -d
{"iss":"scotch.io","exp":1300819380,"name":"Chris Sevilleja","admin":true}
```

## The signature

The signature of a JWT is critical, because it guarantees the integrity of the payload and the header. Verifying the signature must be the first step that any consumer of a JWT performs. If the signature doesn’t match, no further processing should take place.


- header and payload are base64 encoded and concatenated with a .
- the resulting string + a secret key are used to compute a cryptographic signature
- the signature is base64 encoded

The signature is computed by hashing a secret key, the JWT header and the JWT payload. Therefore any tampering with the token will make it invalid. 

## Dangers

- Tokens can be used for their whole lifetime and there is no easy way for the server to invalidate the session. So if a user logs out, the token is valid until the end of its lifetime.
- the same as above goes for blocking users
