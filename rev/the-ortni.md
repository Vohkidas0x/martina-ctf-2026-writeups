# [INTRO] The Ortni — A hidden return-value bug in Python bytecode

**Category:** Reverse engineering · **Status:** Flag candidate reconstructed; accepted submission **not separately documented**  
**Tools:** `strings`, `pyinstxtractor`, Python 3.15, `marshal`, `dis`

## Core insight

A Windows executable packaged with PyInstaller validated a password and printed a processed string. The accompanying PDF already contained the value the program printed, but that value had reportedly been rejected. Disassembling the extracted Python bytecode exposed a subtle bug in `styler4`.

## Method

1. Recognize PyInstaller with `strings`; extract the bundled `FlagSummoner9001.pyc`.
2. Use a Python interpreter matching the bytecode version to load and inspect it with `marshal` and `dis`.
3. Trace the chain `styler1` through `styler5` and observe that `styler4` **calculates a Caesar +3 shift** into a new local but mistakenly **returns the old string**.
4. Apply the otherwise-unused shift to derive the intended result.

```python
# Simplified illustration of the bug:
def styler4(flag):
    flag2 = ''.join(chr(ord(c) + 3) if c.isalpha() else c for c in flag)
    return flag  # incorrect variable; flag2 was discarded
```

**Code-derived candidate:** `MCTF26{wk3_ju34w35w_io4j_0i_4oo_w1p3_9001}`

**Takeaway:** A program's displayed output need not match the intended algorithm. Bytecode can expose a one-variable logic error that is easy to miss in decompiler output.
