# Telekom

Some facts about Telekom fiber using the Telekom's provided ONT:

- the ONT handles authentication against Telekom
- no need for PPPoE credentials on the router behind the ONT
- yet some dummy credentials still need to be used
  - otherwise Telekom rejects the PPPoE connection
  - a random username (e.g. foobar) suffices 
