# Wielder of Names — Finding hidden names through NSEC3

**Category:** Cryptography / DNS security · **Status:** Flag recovered from DNS TXT response  
**Tools:** `dig`, Python, SHA-1, DNS wire-format encoding

## Core insight

The challenge was a DNS zone called `wheel.`. TXT clues described three nested “rings,” each four characters long. A zone transfer failed, but DNSSEC **NSEC3 denial-of-existence records** exposed hashes of domain names, enabling candidate labels to be tested offline.

## Method

1. Query the service and find the zone's SOA record and TXT hints, including the four-character constraint.
2. Request DNSSEC-related responses and inspect NSEC3 records: **SHA-1**, no additional iterations, empty salt.
3. Compute SHA-1 over each lowercase candidate **DNS wire-format** name (including label-length bytes and root terminator), not over a dotted ASCII string.
4. Try four-character lowercase alphanumeric labels—`36^4` candidates per level—against the relevant NSEC3 hash; extend the suffix after each match.
5. Query each recovered name to reveal the next stage.

Recovered chain:

```text
btb8.wheel.
ykx0.btb8.wheel.
ds4e.ykx0.btb8.wheel.
```

The final name's TXT response contained:

```text
MCTF26{its_all_threek_to_me}
```

**Takeaway:** Hashing DNS names for denial proofs is not equivalent to hiding low-entropy names. Enumerating likely labels offline can be much cheaper than querying the server repeatedly. `+dnssec` requests records but does not by itself validate their signatures.
