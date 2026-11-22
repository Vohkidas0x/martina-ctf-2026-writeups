# Mārtiņa-CTF 2026 | Security Research & Write-ups

**Reverse engineering · Cryptography · Digital forensics · Blockchain security**

During **Mārtiņa-CTF 2026**, I continued working independently after my teammates became inactive following the first day, earning **9,500+ points through solo effort** (event result reported by the participant).

This repository presents a **curated selection** of challenge write-ups and small, reproducible Python tools. It is not a claim that every challenge I investigated was solved. Each case study focuses on **the key observation, the method, the evidence, and the lesson** rather than a long terminal transcript.

## Selected technical write-ups

| Challenge | Area | Main technique | Write-up |
| --- | --- | --- | --- |
| **The Beaver** | Reverse engineering | Replaced an infeasible Turing-machine simulation with a closed-form step count and binary search | [Read](rev/the-beaver.md) |
| **The Bouquet** | Digital forensics | Repaired a disguised VeraCrypt header, decrypted FAT16, and recovered a deleted keyfile | [Read](forensics/the-bouquet.md) |
| **Wielder of Names** | DNS / cryptography | Used DNSSEC NSEC3 denial proofs and offline SHA-1 candidate testing to recover nested names | [Read](crypto/wielder-of-names.md) |
| **The Fortune Teller (II)** | Reverse engineering | Patched an unconditional x86-64 jump to reach otherwise skipped code | [Read](rev/fortune-teller-ii.md) |
| **The Grimoire** | Blockchain | Read on-chain storage and used a relay contract to satisfy an unusual caller check | [Read](blockchain/the-grimoire.md) |
| **The Apprentice's Cipher** | Cryptography | Solved chained Caesar, Vigenère, and single-byte XOR stages | [Read](crypto/apprentices-cipher.md) |
| **The Ortni** | Reverse engineering | Disassembled extracted Python bytecode and identified a return-value bug; submission unverified | [Read](rev/the-ortni.md) |

**Also explored:** smart-contract signature malleability, USB HID packet reconstruction, Godot game logic, video analysis, and image geolocation. These are honestly labeled [investigations, not completed solves](investigations/README.md).

## Tools and methods

`Python` · `objdump` · `Linux / WSL` · `Foundry (cast / forge)` · `Wireshark` · `dig` · `FFmpeg` · `ExifTool` · `VeraCrypt` · `Solidity` · `DNSSEC / NSEC3`

## Reproducing the included scripts

The three scripts in [`scripts/`](scripts/) correspond to challenge-supplied binaries/containers, which are **not redistributed** here. Download the original challenge materials if the organizers permit it, then run:

```bash
python3 -m pip install -r requirements.txt  # cryptography, for The Bouquet
python3 scripts/recover_bouquet.py path/to/martina-bouquet.bin
python3 scripts/patch_fortuneteller.py path/to/fortuneteller
python3 scripts/solve_beaver.py path/to/beaver
```

The scripts use offsets and structures from the original challenge versions. Reproduction against other binaries is not expected to work.

## About the results

- **Recovered flags** in this collection were obtained from challenge output or locally reconstructed challenge data. A recovered flag alone does not independently establish a scoreboard acceptance; acceptance evidence is retained only where recorded in the source notes.
- **The Ortni** has a code-derived candidate without a separately recorded accepted submission. It is marked accordingly.
- **Investigations** and candidate coordinates are *not* represented as successful solves.
- Individual point values were excluded because the uploaded drafts contain differing values and the event uses dynamic scoring. The **9,500+** event total is based on the participant's account rather than a preserved scoreboard screenshot.

For publishing instructions see [PUBLISHING.md](PUBLISHING.md). This work documents authorized CTF targets only; no private keys, live access tokens, or original large challenge binaries are included.
