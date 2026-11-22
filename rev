# The Fortune Teller (II) — Unlocking skipped x86-64 code

**Category:** Reverse engineering · **Status:** Flag recovered in patched local executable  
**Tools:** `objdump`, binary patching, Python, Linux / WSL

## Core insight

The provided stripped, PIE ELF looked as though it performed an elaborate “worthiness” calculation. The real obstacle was a **five-byte unconditional jump** at file offset `0x15d2`, skipping the interesting block entirely.

## Method

An `objdump -d -M intel` inspection showed a `jmp` to the function epilogue just before the skipped instructions. I replaced the five-byte `E9 F9 00 00 00` jump with five `0x90` NOP instructions, allowing normal execution to continue into the hidden block.

```bash
python3 scripts/patch_fortuneteller.py path/to/fortuneteller
# Run the newly created 'fortuneteller_patched' on Linux/WSL
```

The script checks the expected original bytes before patching to avoid modifying an unexpected binary version. The patched executable prints:

```text
MCTF26{1_4m_4lw4yS_w0rThy}
```

**Takeaway:** Trace control flow before interpreting complex calculations; unreachable code can be the entire challenge.

[View patch script](../scripts/patch_fortuneteller.py)
