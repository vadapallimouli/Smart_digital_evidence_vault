"""
app.py -- tiny Flask server for MerkleVault.

The HTML front-end (static/index.html) keeps the same screens, login, case
workflow, approvals and reports as before. Every DSA operation is now done
here in Python by the classes in dsa.py:

    POST /api/upload          SHA-256, duplicate / tamper / filename checks, classify, store
    GET  /api/evidence        list of stored evidence
    GET  /api/search?q=       Trie prefix search
    GET  /api/merkle/<case>   Merkle tree (recomputed from current bytes)
    POST /api/seal/<case>     lock the Merkle root
    POST /api/verify/<ev>     re-hash one file
    POST /api/tamper-sim/<ev> flip a byte (demo)
    GET  /api/file/<ev>       open the stored evidence file
    POST /api/sign            SHA-256 digital signature of the final report

Run:   pip install -r requirements.txt   then   python app.py
Open:  http://localhost:5000
"""

import io

from flask import Flask, jsonify, request, send_file, send_from_directory

from dsa import EvidenceVault, sha256_text

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config["MAX_CONTENT_LENGTH"] = 512 * 1024 * 1024      # 512 MB per request

vault = EvidenceVault()


@app.get("/")
def index():
    return send_from_directory("static", "index.html")


@app.get("/api/health")
def health():
    return jsonify(ok=True, engine="python")


@app.post("/api/reset")
def reset():
    """The page calls this on load so a refreshed page starts with an empty vault."""
    vault.reset()
    return jsonify(ok=True)


@app.post("/api/upload")
def upload():
    f = request.files.get("file")
    if f is None:
        return jsonify(error="no file"), 400
    keywords = [k.strip() for k in request.form.get("keywords", "").split(",") if k.strip()]
    result = vault.ingest(
        case_id=request.form.get("caseId", ""),
        case_title=request.form.get("caseTitle", ""),
        filename=f.filename,
        data=f.read(),
        mime=f.mimetype,
        keywords=keywords,
        uploaded_by=request.form.get("uploadedBy", ""),
    )
    return jsonify(result)


@app.get("/api/evidence")
def evidence():
    return jsonify(evidence=[e.to_dict() for e in vault.evidence.values()],
                   trieNodes=vault.trie.node_count)


@app.get("/api/search")
def search():
    return jsonify(ids=vault.search(request.args.get("q", "")), trieNodes=vault.trie.node_count)


@app.get("/api/merkle/<case_id>")
def merkle(case_id):
    return jsonify(vault.case_tree(case_id, update_status=request.args.get("verify") == "1"))


@app.post("/api/seal/<case_id>")
def seal(case_id):
    return jsonify(root=vault.seal(case_id))


@app.post("/api/verify/<ev_id>")
def verify(ev_id):
    if ev_id not in vault.evidence:
        return jsonify(error="unknown evidence"), 404
    return jsonify(status=vault.verify_evidence(ev_id))


@app.post("/api/tamper-sim/<ev_id>")
def tamper_sim(ev_id):
    if ev_id not in vault.evidence:
        return jsonify(error="unknown evidence"), 404
    vault.simulate_tamper(ev_id)
    return jsonify(ok=True)


@app.get("/api/file/<ev_id>")
def file(ev_id):
    ev = vault.evidence.get(ev_id)
    if ev is None:
        return jsonify(error="unknown evidence"), 404
    mime = ev.mime if ev.mime and ev.mime != "unknown" else "application/octet-stream"
    return send_file(io.BytesIO(ev.current_bytes()), mimetype=mime, download_name=ev.name)


@app.post("/api/sign")
def sign():
    payload = (request.get_json(silent=True) or {}).get("payload", "")
    return jsonify(signature=sha256_text(payload))


if __name__ == "__main__":
    print("MerkleVault running ->  http://localhost:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
