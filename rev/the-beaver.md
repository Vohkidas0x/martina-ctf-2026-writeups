# The Beaver — Reverse engineering a giant Turing-machine run

**Category:** Reverse engineering · **Status:** Flag recovered from the supplied challenge binary  
**Tools:** Python, binary analysis, integer arithmetic

## Core insight

The binary implements an eight-state, two-symbol Turing machine that behaves like a **binary counter**, but its step limit is approximately **3.7 × 10^87**. Simulating that many transitions is impossible in practice. I recovered the transition table and replaced the simulation with a count of complete counter increments.

## Method

The transition table starts at file offset `0x2000`; the limit is stored in five little-endian 64-bit limbs at `0x2030:0x2058`. At the counter's stable macrostate, the number of machine transitions required for `n` increments is:

```text
T(n) = 5*n - 4*popcount(n) + (n & 1)
```

I verified the formula against direct simulation at smaller step counts, then used binary search for the largest `n` with `T(n) <= limit`. For the challenge's limit, exactly one transition remained and `n` was even. That step sets the low bit, so the final counter value is `n + 1`. Interpreting its bits as little-endian bytes revealed the flag.

```bash
python3 scripts/solve_beaver.py path/to/beaver
```

**Recovered flag:** `MCTF26{Bu5y_Be4v3r_of_5_is_n0t_7h1s}`

**Takeaway:** A huge deterministic computation may be tractable through an invariant and a closed-form model, not faster simulation.

[View Python solver](../scripts/solve_beaver.py)
