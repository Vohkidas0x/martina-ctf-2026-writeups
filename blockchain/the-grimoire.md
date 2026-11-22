# The Grimoire — Public storage and contract-call identity

**Category:** Blockchain / EVM security · **Status:** Challenge flag returned by the instance  
**Tools:** Foundry (`cast`, `forge`), EVM bytecode inspection, Solidity

## Core insight

This contract checked a “secret” word and restricted who could submit it. Bytecode analysis showed that the word was stored in an ordinary Solidity mapping, and a separate condition required `tx.origin != msg.sender`.

## Method

1. Locate the underlying challenge contract from the setup contract's bytecode.
2. Recover the selector for the call that accepted a `uint256` word, and inspect the embedded revert strings.
3. Trace `KECCAK256`/`SLOAD` to identify the mapping lookup: **key `7` in mapping slot `2`**. Compute the entry location, then read it with `cast storage`.
4. Deploy a minimal relay contract, then call the target through the relay. The transaction originates from my wallet (`tx.origin`), while the target sees the relay as `msg.sender`.
5. Verify `isOpen()` and request the flag from the CTF menu.

To derive the mapping entry's storage location with Foundry:

```bash
cast index uint256 7 2
# 0xacd8ef244210bb6898e73c48bf820ed8ecc857a3bab8d79c10e4fa92b1e9ca65
# cast storage <target-contract> <derived-slot> --rpc-url <challenge-RPC>
```

This order matches the recovered hash in my original notes: `cast index <key-type> <key> <mapping-slot>`.

The access check is illustrated by:

```solidity
// Called from an externally-owned account, this is false.
// Called through a helper contract, it can be true.
require(tx.origin != msg.sender, "Only a familiar may speak the word");
```

**Recovered flag:** `MCTF26{pr1v4t3_p4g3s_4r3_publ1c_f53d19}`

**Takeaway:** Solidity `private` does not encrypt on-chain storage. Also, `tx.origin` and `msg.sender` represent different callers when a contract forwards a call.
