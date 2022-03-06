
## RSA

RSA was the first public key cryptography system. It based on the fact that multiplication is fast and factorisation is (very) slow. Basically a RSA system works as follows:

1. pick two prime numbers: `r` and `q`
2. multiply those numbers to obtain a an max value: `r*q=max` under the condition that `max` is greater than the largest value that we are going to encrypt
3. pick a random prime as a public key with the condition: `0<pub<max`
4. compute the private key `priv` using extended eucliean algorithm
5. in order to encrypt a value do the following:
    1. multiply the value by itself `pub` times whie wraping around the maximum for each multiplication (modulo)
6. to get the actual value back:
    1. multiply the cypher by itself `prive` times whie wraping around the maximum for each multiplication (modulo)

## Sample implementation in Python

```python
# requires pycryptodome (pip install pycryptodome)

from Crypto.Util.number import inverse


def euclidean(pub, x, y):
    phi = (x - 1) * (y - 1)
    return inverse(pub, phi)


def mlt(v, p, vmax):
    t = v
    for _ in range(p - 1):
        t = (t*v) % vmax
    return t


def enc(text, p, vmax):
    cypher = ""
    for c in text:
        cypher += chr(mlt(ord(c),p,vmax))
    
    return cypher


def main():
    # Basic setup
    r = 13
    q = 23
    vmax = r * q  # 299 <- is larger than 255 so any ascii value can be encrypted

    # Let pub be any prime < vmax and compute priv
    pub = 5
    priv = euclidean(pub, r, q)

    print(f"public key: {pub:d}")
    print(f"private key: {priv:d}")

    text = "Hello, World!"

    cypher = enc(text, pub, vmax)

    print(enc(cypher, priv, vmax)) # <- outputs hello world


main()
```