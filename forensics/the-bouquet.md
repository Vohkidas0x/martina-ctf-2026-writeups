# The Bouquet — Recovering a hidden VeraCrypt volume

**Category:** Forensics / cryptography · **Status:** Flag recovered from challenge volume  
**Tools:** Python, `cryptography`, VeraCrypt concepts, FAT16 analysis

## Core insight

The 16 MiB input looked unrecognizable because its **first 64 bytes**—the VeraCrypt salt—were XORed with `0x88`. Applying the XOR to the whole file damaged the encrypted payload; restoring only the salt made the standard container structure recoverable.

## Method

1. XOR just bytes `0:64` with `0x88` to restore the header salt.
2. Derive the header key with PBKDF2-HMAC-SHA512 using the supplied challenge password, then decrypt the VeraCrypt header via AES-XTS and verify `VERA`.
3. Decrypt the outer FAT16 volume and recover an important **deleted PNG file**.
4. Follow a Caesar-cipher clue to obtain the hidden volume's password, **`The die is cast`**; use the recovered `BOUQUET.PNG` as the VeraCrypt keyfile.
5. Read `FLAG.txt` from the hidden FAT12 filesystem.

The accompanying Python script automates the salt restoration, outer-volume decryption, and initial filesystem recovery; the hidden-volume opening is a separate step.

```bash
python3 -m pip install -r requirements.txt
python3 scripts/recover_bouquet.py path/to/martina-bouquet.bin
```

**Recovered flag:** `MCTF26{1_c4st_1n5t4nt_d4t4_l055}`

**Takeaway:** Distinguish header-level obfuscation from encryption. A deleted file can be security-critical when reused as a keyfile.

[View recovery script](../scripts/recover_bouquet.py)
