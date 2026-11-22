# The Apprentice's Cipher — Three chained ciphers

**Category:** Cryptography · **Status:** Flag decoded from the challenge  
**Tools:** Python, Caesar, Vigenère, single-byte XOR

## Core insight

Three consecutive “seals” used simple classical ciphers. Each plaintext supplied the context needed to attack the next stage, ending with a known-plaintext attack against XOR.

## Method

1. **Caesar:** Brute-force 25 nontrivial shifts. Shifting backwards by seven reveals a hint about the Archmage's familiar.
2. **Vigenère:** Use the narrative clue **`QUILL`** as the repeating keyword. Decryption says that every flag begins the same way.
3. **Single-byte XOR:** Use the known flag prefix `MCTF26{` to derive the XOR byte (`0x5a`) and decode the final seal.

```python
# One known plaintext byte can determine a single-byte XOR key.
ciphertext = bytes.fromhex("17190e1c686c213169232905376e2e2e6928056e2a2a2869342e6b396927")
key = ciphertext[0] ^ ord('M')  # -> 0x5a for this challenge
plaintext = bytes(b ^ key for b in ciphertext)
print(plaintext.decode())
```

**Recovered flag:** `MCTF26{k3ys_m4tt3r_4ppr3nt1c3}`

**Takeaway:** Small keyspaces, reused contextual clues, and predictable plaintext make classical encryption easy to break.
