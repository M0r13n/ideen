# Hashcash

> The idea "...to require a user to compute a moderately hard, but not intractable function..." was proposed by Cynthia Dwork and Moni Naor in their 1992 paper "Pricing via Processing or Combatting Junk Mail"

- Proof-Of-Work system
- used to limit Spam and dos attacks
- [technical details](https://en.wikipedia.org/wiki/Hashcash)
- [my implementation](https://gist.github.com/M0r13n/f8fc71bc57b475c9841a663da57ec504)
- each header contains a random sequence of characters (a salt)
  - used to prevent double spending
  - either by remembering all seen salts on the server side
  - or by sending a challenge to client
    - also needs to remembered by the server
- header contains resource and date fields to further force uniqueness
- computational effort increases exponentially with he number of bits