"""
dsa.py  --  Data Structures & Algorithms of MerkleVault (pure Python)
=====================================================================

Everything the project's "DSA part" does lives in this one file:

    1. SHA-256 fingerprinting ............ hashlib
    2. Hash Map (dict) ................... exact-duplicate lookup, O(1)
    3. Trie (prefix tree) ................ evidence search, O(length of query)
    4. Merkle Tree ....................... integrity verification, O(n) build
    5. Content-defined chunking .......... remembers file CONTENT (gear hash)
    6. Set / Map similarity .............. detects modified (tampered) copies
    7. File classification ............... Image / Video / Audio / PDF / Document
    8. EvidenceVault ..................... ties all of the above into one pipeline

app.py (Flask) only exposes these classes to the HTML front-end.
You can also run   python demo.py   to see every algorithm work in the terminal.
"""

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime


# ---------------------------------------------------------------------------
# 1. SHA-256 FINGERPRINT
# ---------------------------------------------------------------------------
# SHA-256 turns any file into a 64-character hexadecimal fingerprint.
# Identical bytes  -> identical fingerprint.
# Any 1-bit change -> a completely different fingerprint.

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def short_hash(h: str) -> str:
    return h[:10] + "…" + h[-8:] if h else ""


# ---------------------------------------------------------------------------
# 2. TRIE  (prefix tree)  --  fast evidence search
# ---------------------------------------------------------------------------
# Each node stores its children in a dict (character -> node) and a set of
# evidence IDs that pass through that node. To search a prefix we walk one
# node per character, so the time is O(length of the query) no matter how
# many evidence files are stored.

class TrieNode:
    def __init__(self):
        self.children = {}      # char -> TrieNode
        self.refs = set()       # evidence ids reachable through this node


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.node_count = 1

    def insert(self, word: str, ref: str) -> None:
        if not word:
            return
        node = self.root
        for ch in word.lower():
            if ch not in node.children:
                node.children[ch] = TrieNode()
                self.node_count += 1
            node = node.children[ch]
            node.refs.add(ref)

    def search_prefix(self, prefix: str) -> set:
        node = self.root
        for ch in prefix.lower():
            if ch not in node.children:
                return set()
            node = node.children[ch]
        return set(node.refs)


# ---------------------------------------------------------------------------
# 3. MERKLE TREE  --  integrity verification
# ---------------------------------------------------------------------------
# Leaves  = the SHA-256 fingerprints of the evidence files.
# Parents = SHA-256( left_child + right_child ).
# If a level has an odd number of nodes, the last node is paired with itself.
# The single hash at the top is the MERKLE ROOT: if even one byte of one file
# changes, the root changes -- so one value proves the whole case is intact.

def build_merkle_tree(hashes: list):
    """Return (levels, root).  levels[0] = leaves ... levels[-1] = [root]."""
    if not hashes:
        return [], None
    level = list(hashes)
    levels = [level]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else level[i]
            nxt.append(sha256_text(left + right))
        levels.append(nxt)
        level = nxt
    return levels, level[0]


# ---------------------------------------------------------------------------
# 4. CONTENT-DEFINED CHUNKING  --  the vault "remembers" file content
# ---------------------------------------------------------------------------
# A plain hash only says "same" or "different". To notice that a file is an
# EDITED copy of one we already hold (slides removed, text replaced ...) we
# cut every file into chunks and remember a fingerprint of each chunk.
#
# Chunk boundaries are decided by the CONTENT (a rolling "gear" hash), not by
# fixed positions. So if bytes are deleted in the middle of a file, the chunks
# before and after the edit are cut at the same places and still match.

def _make_gear_table():
    """256 pseudo-random 32-bit numbers (xorshift32), one per byte value."""
    table, x = [], 0x9E3779B9
    for _ in range(256):
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= x >> 17
        x ^= (x << 5) & 0xFFFFFFFF
        x &= 0xFFFFFFFF
        table.append(x)
    return table


GEAR = _make_gear_table()


@dataclass(frozen=True)
class ChunkParams:
    key: str
    min_size: int
    mask: int
    max_size: int


def chunk_params(size: int) -> ChunkParams:
    """Smaller chunks for small files, larger chunks for big files."""
    if size < 65_536:
        return ChunkParams("s", 16, 0x3F, 256)
    if size < 4_194_304:
        return ChunkParams("m", 256, 0x3FF, 4096)
    return ChunkParams("l", 1024, 0xFFF, 16384)


def chunk_bytes(data: bytes, p: ChunkParams) -> dict:
    """
    Split `data` into content-defined chunks.
    Returns a dict (hash map):  chunk-fingerprint -> total bytes of that chunk.
    """
    chunks = {}
    start, h, n = 0, 0, len(data)
    gear, mask, min_size, max_size = GEAR, p.mask, p.min_size, p.max_size
    for i in range(n):
        h = (((h << 1) & 0xFFFFFFFF) + gear[data[i]]) & 0xFFFFFFFF   # rolling hash
        length = i - start + 1
        if (length >= min_size and (h & mask) == 0) or length >= max_size or i == n - 1:
            fp = hashlib.sha1(data[start:i + 1]).hexdigest()[:16]    # chunk fingerprint
            chunks[fp] = chunks.get(fp, 0) + length
            start, h = i + 1, 0
    return chunks


# ---------------------------------------------------------------------------
# 5. SIMILARITY  --  how much of an old file survives inside a new one?
# ---------------------------------------------------------------------------

@dataclass
class Similarity:
    ratio_new: float      # share of the NEW file that came from the old file
    ratio_old: float      # share of the OLD file still present in the new file
    shared_chunks: int


def similarity(new_chunks: dict, old_chunks: dict) -> Similarity:
    new_total = sum(new_chunks.values())
    old_total = sum(old_chunks.values())
    shared = shared_chunks = 0
    for fp, size in new_chunks.items():            # set-intersection style lookup
        if fp in old_chunks:
            shared += min(size, old_chunks[fp])
            shared_chunks += 1
    return Similarity(
        ratio_new=shared / new_total if new_total else 0.0,
        ratio_old=shared / old_total if old_total else 0.0,
        shared_chunks=shared_chunks,
    )


def pct(x: float) -> int:
    return int(x * 100 + 0.5)


# ---------------------------------------------------------------------------
# 6. FILE CLASSIFICATION
# ---------------------------------------------------------------------------

def classify(mime: str, name: str) -> str:
    mime = mime or ""
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else name.lower()
    if mime.startswith("image/"):
        return "Image"
    if mime.startswith("video/"):
        return "Video"
    if mime.startswith("audio/"):
        return "Audio"
    if mime == "application/pdf" or ext == "pdf":
        return "PDF"
    return "Document"


def base_name(name: str) -> str:
    """'Syllabus.PNG' -> 'syllabus'  (name without extension, lower-case)."""
    return re.sub(r"\.[^.]*$", "", name).strip().lower()


# ---------------------------------------------------------------------------
# 7. EVIDENCE VAULT  --  the whole upload pipeline
# ---------------------------------------------------------------------------

@dataclass
class Evidence:
    id: str
    case_id: str
    name: str
    size: int
    mime: str
    category: str
    hash: str
    keywords: list
    uploaded_at: str
    uploaded_by: str
    data: bytes = field(repr=False)
    status: str = "verified"
    tampered_data: bytes = field(default=None, repr=False)
    fingerprints: dict = field(default_factory=dict, repr=False)   # chunk cache
    tamper_attempts: int = 0

    def current_bytes(self) -> bytes:
        return self.tampered_data if self.tampered_data is not None else self.data

    def chunks(self, p: ChunkParams) -> dict:
        if p.key not in self.fingerprints:
            self.fingerprints[p.key] = chunk_bytes(self.data, p)
        return self.fingerprints[p.key]

    def to_dict(self) -> dict:
        return {
            "id": self.id, "caseId": self.case_id, "name": self.name, "size": self.size,
            "mime": self.mime, "category": self.category, "hash": self.hash,
            "keywords": self.keywords, "uploadedAt": self.uploaded_at,
            "uploadedBy": self.uploaded_by, "status": self.status,
            "tamperAttempts": self.tamper_attempts,
        }


class EvidenceVault:
    def __init__(self):
        self.reset()

    def reset(self):
        self.evidence = {}      # id        -> Evidence            (dict keeps upload order)
        self.hash_index = {}    # sha256    -> evidence id         HASH MAP: exact duplicates
        self.name_index = {}    # base name -> evidence id         HASH MAP: filename conflicts
        self.case_index = {}    # case id   -> [evidence ids]      HASH MAP of lists
        self.seals = {}         # case id   -> sealed Merkle root
        self.trie = Trie()      # TRIE: search
        self.next_ev_num = 1

    # ---- upload pipeline --------------------------------------------------
    def ingest(self, case_id, case_title, filename, data, mime, keywords, uploaded_by):
        """
        SHA-256 -> exact duplicate? -> modified copy? -> filename conflict? -> store
        Returns a dict whose "status" is one of:
            duplicate | tampered | name_conflict | stored
        """
        digest = sha256_bytes(data)

        # (1) EXACT DUPLICATE: same bytes, whatever the filename.  O(1) hash-map lookup.
        if digest in self.hash_index:
            existing = self.evidence[self.hash_index[digest]]
            return {"status": "duplicate", "hash": digest,
                    "existing": self._ref(existing),
                    "renamed": existing.name != filename}

        # (2) MODIFIED COPY: compare chunk fingerprints with everything we remember.
        params = chunk_params(len(data))
        new_chunks = chunk_bytes(data, params)
        best = None
        for ev in self.evidence.values():
            sim = similarity(new_chunks, ev.chunks(params))
            score = max(sim.ratio_new, sim.ratio_old)
            if best is None or score > best[2]:
                best = (ev, sim, score)

        if best and ((best[1].shared_chunks >= 2 and best[2] >= 0.25) or best[2] >= 0.5):
            ref, sim, _ = best
            ref.tamper_attempts += 1
            intact = pct(sim.ratio_old)
            return {"status": "tampered", "hash": digest,
                    "existing": self._ref(ref),
                    "intact": intact, "removed": 100 - intact,
                    "added": pct(1 - sim.ratio_new),
                    "sameName": ref.name.lower() == filename.lower()}

        # (2b) FILENAME CONFLICT: name (without extension) already used, content unrelated.
        owner_id = self.name_index.get(base_name(filename))
        if owner_id:
            return {"status": "name_conflict", "hash": digest,
                    "existing": self._ref(self.evidence[owner_id])}

        # (3) GENUINELY NEW EVIDENCE -> classify, store, index
        ev_id = "EV-%04d" % self.next_ev_num
        self.next_ev_num += 1
        ev = Evidence(
            id=ev_id, case_id=case_id, name=filename, size=len(data), mime=mime or "unknown",
            category=classify(mime, filename), hash=digest, keywords=keywords,
            uploaded_at=datetime.now().astimezone().isoformat(), uploaded_by=uploaded_by, data=data)
        ev.fingerprints[params.key] = new_chunks
        self.evidence[ev_id] = ev
        self.hash_index[digest] = ev_id
        self.name_index[base_name(filename)] = ev_id
        self.case_index.setdefault(case_id, []).append(ev_id)
        self._index_for_search(ev, case_title)
        return {"status": "stored", "evidence": ev.to_dict()}

    @staticmethod
    def _ref(ev):
        return {"id": ev.id, "name": ev.name, "caseId": ev.case_id}

    # ---- Trie search ------------------------------------------------------
    def _index_for_search(self, ev, case_title):
        t = self.trie
        t.insert(ev.id, ev.id)
        for tok in re.split(r"[\s._-]+", ev.name):
            t.insert(tok, ev.id)
        t.insert(ev.case_id, ev.id)
        for tok in re.split(r"[\s-]+", case_title or ""):
            t.insert(tok, ev.id)
        for kw in ev.keywords:
            t.insert(kw, ev.id)

    def search(self, prefix):
        return sorted(self.trie.search_prefix(prefix))

    # ---- Merkle tree / integrity -----------------------------------------
    def items_of(self, case_id):
        return [self.evidence[i] for i in self.case_index.get(case_id, [])]

    def case_tree(self, case_id, update_status=False):
        """Recompute every fingerprint from the CURRENT bytes and rebuild the tree."""
        items = self.items_of(case_id)
        current = [sha256_bytes(e.current_bytes()) for e in items]
        bad = [cur != e.hash for cur, e in zip(current, items)]
        if update_status:
            for e, is_bad in zip(items, bad):
                e.status = "tampered" if is_bad else "verified"
        levels, root = build_merkle_tree(current)
        return {"items": [e.to_dict() for e in items], "cur": current, "bad": bad,
                "levels": levels, "root": root, "sealedRoot": self.seals.get(case_id)}

    def seal(self, case_id):
        root = self.case_tree(case_id)["root"]
        if root:
            self.seals[case_id] = root
        return root

    def verify_evidence(self, ev_id):
        ev = self.evidence[ev_id]
        ev.status = "verified" if sha256_bytes(ev.current_bytes()) == ev.hash else "tampered"
        return ev.status

    def simulate_tamper(self, ev_id):
        """Demo only: flip the first byte so verification will fail."""
        ev = self.evidence[ev_id]
        b = bytearray(ev.data)
        if b:
            b[0] ^= 0xFF
        else:
            b = bytearray([1])
        ev.tampered_data = bytes(b)
        ev.status = "unverified"
