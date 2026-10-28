# MerkleVault — Smart Digital Evidence Management (Python DSA edition)

The screens, login (3 departments × 4 authorities), 13-step approval workflow,
case reports and digital signature are exactly as before (`static/index.html`).
**Every data-structure / algorithm operation now runs in Python** (`dsa.py`).

## Run

```bash
pip install -r requirements.txt
python app.py            # then open  http://localhost:5000
```

Do **not** open `static/index.html` by double-clicking — it needs the Python server.
To see the algorithms in the terminal only (no browser):  `python demo.py`

## Files

| File | What it is |
|---|---|
| `dsa.py` | All DSA code: SHA-256, Hash Map, Trie, Merkle Tree, content chunking, similarity, classification, `EvidenceVault` |
| `app.py` | Small Flask server that exposes `dsa.py` to the HTML page |
| `static/index.html` | The user interface (login, dashboards, workflow, reports) |
| `demo.py` | Terminal walk-through of every algorithm |

## How to explain each DSA to your faculty

| Concept | Where in `dsa.py` | Idea | Complexity |
|---|---|---|---|
| **SHA-256** | `sha256_bytes()` | File → 64-hex fingerprint; any change gives a different one | O(file size) |
| **Hash Map** | `EvidenceVault.hash_index`, `name_index`, `case_index` (Python `dict`) | Fingerprint → evidence id, so an exact duplicate is found instantly | O(1) |
| **Trie** | `class Trie`, `TrieNode` | Evidence names / ids / keywords stored letter by letter; prefix search walks one node per letter | O(length of query) |
| **Merkle Tree** | `build_merkle_tree()` | Leaves = file hashes, parent = SHA-256(left+right); the root proves the whole case is unchanged | O(n) build |
| **Content-defined chunking** | `chunk_bytes()` | A rolling *gear hash* decides chunk boundaries from the content, so deleting bytes in the middle does not shift later chunks | O(file size) |
| **Set/Map similarity** | `similarity()` | Share of old chunks still present in the new file → "80 % intact" | O(chunks) |
| **Classification** | `classify()` | MIME type / extension → Image, Video, Audio, PDF, Document | O(1) |

## Upload pipeline (`EvidenceVault.ingest`)

```
SHA-256  →  exact duplicate?  →  edited copy of stored evidence?  →  filename already used?  →  classify + store + Trie index
            (hash map)           (chunk similarity ≥ 25 %)            (name without extension)
```

| Result | Meaning |
|---|---|
| `duplicate` | identical bytes (any filename) |
| `tampered` | content partly matches stored evidence (some removed/replaced) — the case gets a tamper alert and cannot be sealed until an Inspector/DSP/SP resolves it |
| `name_conflict` | same name (ignoring extension), different content → "please change the file name" |
| `stored` | new evidence |

## Limits (be upfront in the review)

* Modified-copy detection needs ≥ 25 % shared content; images/videos that are re-saved or re-encoded change every byte and cannot be matched this way.
* The vault lives in server memory for the session (refreshing the page starts a clean vault). A production system would persist to a database/encrypted storage.
