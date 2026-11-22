#!/usr/bin/env python3
"""MCTF26 - The Beaver: fast-forward the binary-counter Turing machine."""
from pathlib import Path
import re
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else 'beaver')
data = path.read_bytes()

# Five little-endian uint64 limbs at file offset 0x2030.
limit = int.from_bytes(data[0x2030:0x2058], 'little')


def steps(n: int) -> int:
    """Steps until n increments are complete and head/state return to zero."""
    return 5 * n - 4 * n.bit_count() + (n & 1)

# Largest n whose macrostate has been reached by the instruction limit.
lo, hi = 0, limit
while lo < hi:
    mid = (lo + hi + 1) // 2
    if steps(mid) <= limit:
        lo = mid
    else:
        hi = mid - 1

n = lo
remainder = limit - steps(n)
print(f'[+] Completed increments: {n}')
print(f'[+] Steps into next increment: {remainder}')

# On this challenge, n is even and exactly one step remains: state 0
# flips the least significant tape bit from 0 to 1.
assert n % 2 == 0 and remainder == 1, 'Unexpected partial Turing-machine state'
value = n + 1
out = value.to_bytes((value.bit_length() + 7) // 8, 'little')
print(f'[+] Decoded bytes: {out!r}')
match = re.search(rb'MCTF26\{[^}]+\}', out)
assert match, 'Flag not found'
print('[FLAG]', match.group().decode())
