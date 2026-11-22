#!/usr/bin/env python3
"""MCTF26 - The Bouquet: restore salt, decrypt outer VeraCrypt volume, recover files.

Requires: pip install cryptography
Usage: python3 scripts/recover_bouquet.py martina-bouquet.bin
The hidden volume still needs password 'The die is cast' and the recovered
BOUQUET.PNG as a VeraCrypt keyfile; this script extracts the outer clues.
"""
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib
import sys

source = Path(sys.argv[1] if len(sys.argv) > 1 else 'martina-bouquet.bin')
data = bytearray(source.read_bytes())
if len(data) != 16777216:
    raise ValueError('Unexpected file size')

# The challenge XORed only the 64-byte VeraCrypt salt, not the whole container.
data[:64] = bytes(b ^ 0x88 for b in data[:64])
salt = bytes(data[:64])
print('[+] Restored salt:', repr(salt.rstrip(b'\0')))

restored = source.with_name('bouquet_restored.hc')
restored.write_bytes(data)
print('[+] Saved mountable volume:', restored)

password = b'MCTF26'
header_key = hashlib.pbkdf2_hmac('sha512', password, salt, 500000, 64)
header = Cipher(algorithms.AES(header_key), modes.XTS(bytes(16))).decryptor().update(bytes(data[64:512]))
assert header.startswith(b'VERA'), 'VeraCrypt header did not authenticate as expected'
print('[+] VeraCrypt VERA signature found')

master_key = header[192:256]
enc_offset = int.from_bytes(header[44:52], 'big')
enc_length = int.from_bytes(header[52:60], 'big')
sector_size = int.from_bytes(header[64:68], 'big')
assert sector_size == 512 and enc_offset == 0x20000
print(f'[+] Encrypted FAT volume: offset={enc_offset:#x}, length={enc_length:#x}')

volume = bytearray()
for offset in range(enc_offset, enc_offset + enc_length, sector_size):
    tweak = (offset // sector_size).to_bytes(16, 'little')
    ctx = Cipher(algorithms.AES(master_key), modes.XTS(tweak)).decryptor()
    volume.extend(ctx.update(bytes(data[offset:offset + sector_size])) + ctx.finalize())
assert b'FAT16' in volume[:90], 'Expected FAT16 filesystem'

save_dir = source.parent / 'bouquet_recovered'
save_dir.mkdir(exist_ok=True)
(save_dir / 'outer_fat16.img').write_bytes(volume)

bps = int.from_bytes(volume[11:13], 'little')
spc = volume[13]
reserved = int.from_bytes(volume[14:16], 'little')
fats = volume[16]
root_entries = int.from_bytes(volume[17:19], 'little')
spf = int.from_bytes(volume[22:24], 'little')
fat_base = reserved * bps
root_base = (reserved + fats * spf) * bps
data_base = root_base + root_entries * 32
cluster_size = bps * spc


def cluster_offset(cluster):
    return data_base + (cluster - 2) * cluster_size


def contents(cluster, size, deleted=False):
    parts = []
    while len(parts) * cluster_size < size:
        parts.append(volume[cluster_offset(cluster):cluster_offset(cluster) + cluster_size])
        if deleted:  # deleted PNG was contiguous; chain is unavailable
            cluster += 1
        else:
            next_cluster = int.from_bytes(volume[fat_base + 2 * cluster:fat_base + 2 * cluster + 2], 'little')
            if next_cluster >= 0xfff8:
                break
            cluster = next_cluster
    return b''.join(parts)[:size]

for offset in range(root_base, root_base + root_entries * 32, 32):
    ent = volume[offset:offset + 32]
    if ent[0] == 0:
        break
    if ent[11] & 0x18:  # volume label or directory
        continue
    deleted = ent[0] == 0xe5
    name = bytes(ent[:8]).decode('ascii', 'replace').strip()
    ext = bytes(ent[8:11]).decode('ascii', 'replace').strip()
    if deleted:
        name = 'BOUQUET'  # deleted entry shown as \xe5OUQUET
    filename = name + ('.' + ext if ext else '')
    cluster = int.from_bytes(ent[26:28], 'little')
    size = int.from_bytes(ent[28:32], 'little')
    if cluster < 2 or not size:
        continue
    saved = save_dir / filename
    saved.write_bytes(contents(cluster, size, deleted))
    print('[+] Recovered:', saved, '(deleted)' if deleted else '')

print('[+] Decode NOTE.TXT with Caesar shift -3. Use recovered BOUQUET.PNG as VeraCrypt keyfile for the hidden volume.')
