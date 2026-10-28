"""
demo.py -- run the whole DSA part in the terminal (no browser needed).

    python demo.py

Shows, step by step:  SHA-256 -> Hash Map -> Trie -> Merkle Tree ->
content memory (tamper detection) -> filename conflict -> integrity check.
"""
import random

from dsa import EvidenceVault, Trie, build_merkle_tree, sha256_bytes, short_hash


def make_file(size, seed):
    return random.Random(seed).randbytes(size)


def title(text):
    print("\n" + "=" * 72 + "\n" + text + "\n" + "=" * 72)


vault = EvidenceVault()

# ---------------------------------------------------------------- 1. SHA-256
title("1. SHA-256 fingerprint")
a = b"The same file content"
b = b"The same file contenT"                      # one character changed
print("original :", sha256_bytes(a))
print("1 char   :", sha256_bytes(b))
print("-> a tiny change gives a completely different fingerprint")

# ------------------------------------------------------- upload first evidence
title("2. Upload evidence  (SHA-256 -> classify -> store -> Trie index)")
dad = make_file(1_000_000, seed=1)                # pretend this is dad.ppt
r = vault.ingest("CASE-001", "Fraud Case", "dad.ppt", dad, "application/vnd.ms-powerpoint", ["slides"], "SI")
print("dad.ppt ->", r["status"], r["evidence"]["id"], r["evidence"]["category"], short_hash(r["evidence"]["hash"]))
r = vault.ingest("CASE-001", "Fraud Case", "photo.png", make_file(200_000, 2), "image/png", [], "SI")
print("photo.png ->", r["status"], r["evidence"]["id"], r["evidence"]["category"])

# ---------------------------------------------------------- 3. exact duplicate
title("3. Hash Map: exact duplicate (any filename)")
r = vault.ingest("CASE-001", "Fraud Case", "friend.ppt", dad, "application/vnd.ms-powerpoint", [], "SI")
print("same bytes, new name 'friend.ppt' ->", r["status"], "| renamed:", r["renamed"],
      "| matches", r["existing"]["id"])

# ------------------------------------------------------------ 4. tamper detect
title("4. Content memory: edited copy (a section removed)")
edited = dad[:400_000] + dad[700_000:]            # 300 KB removed from the middle
r = vault.ingest("CASE-001", "Fraud Case", "dad.ppt", edited, "application/vnd.ms-powerpoint", [], "SI")
print("status:", r["status"], "| original intact:", r["intact"], "% | removed/altered:", r["removed"], "%")
r = vault.ingest("CASE-001", "Fraud Case", "friend2.ppt", edited, "application/vnd.ms-powerpoint", [], "SI")
print("same edit, different name ->", r["status"], "| original intact:", r["intact"], "%")

# ---------------------------------------------------------- 5. name conflict
title("5. Filename conflict (same name, unrelated content)")
r = vault.ingest("CASE-001", "Fraud Case", "Photo.jpeg", make_file(150_000, 99), "image/jpeg", [], "SI")
print("'Photo.jpeg' vs existing 'photo.png' ->", r["status"], "| please rename")

# -------------------------------------------------------------------- 6. Trie
title("6. Trie: prefix search")
print("nodes in trie:", vault.trie.node_count)
for q in ("da", "ph", "ev-0", "fra", "zzz"):
    print(f"  search '{q}' ->", vault.search(q))

# ---------------------------------------------------------------- 7. Merkle
title("7. Merkle tree and integrity verification")
t = vault.case_tree("CASE-001")
for i, lvl in enumerate(reversed(t["levels"])):
    print("  level", i, [short_hash(h) for h in lvl])
root = vault.seal("CASE-001")
print("sealed root:", root)

print("\nVerify again (nothing changed):")
t = vault.case_tree("CASE-001")
print("  root matches sealed root:", t["root"] == vault.seals["CASE-001"])

print("\nNow tamper with EV-0002 (flip one byte) and verify:")
vault.simulate_tamper("EV-0002")
t = vault.case_tree("CASE-001", update_status=True)
print("  per-file tampered flags:", t["bad"])
print("  root matches sealed root:", t["root"] == vault.seals["CASE-001"], "  -> TAMPERING DETECTED")
