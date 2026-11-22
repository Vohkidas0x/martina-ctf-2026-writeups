#!/usr/bin/env python3
"""MCTF26 - The Fortune Teller (II): NOP out the unconditional skip."""
from pathlib import Path
import sys

source = Path(sys.argv[1] if len(sys.argv) > 1 else 'fortuneteller')
out_path = source.with_name('fortuneteller_patched')
code = bytearray(source.read_bytes())
offset = 0x15D2
assert code[offset:offset + 5] == bytes.fromhex('e9f9000000'), 'Unexpected binary/version'
code[offset:offset + 5] = b'\x90' * 5
out_path.write_bytes(code)
out_path.chmod(out_path.stat().st_mode | 0o111)
print(f'Patched {source} -> {out_path}')
print(f'Run on Linux/WSL: ./{out_path.name}')
