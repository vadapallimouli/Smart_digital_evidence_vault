# 🔐 MerkleVault — Smart Digital Evidence Management System

**MerkleVault** is a digital evidence management system designed to securely store, organize, verify, and manage digital evidence. It uses **SHA-256 cryptographic hashing and Merkle Trees** to detect evidence tampering and maintain data integrity.

The system also incorporates data structures and intelligent content-based analysis to identify exact duplicates and potentially modified digital evidence.

## 🎯 Project Objectives

- Securely manage digital evidence associated with individual cases.
- Generate unique cryptographic fingerprints for evidence files.
- Detect unauthorized modifications through hash verification.
- Use Merkle Trees to verify the integrity of multiple evidence files.
- Identify duplicate evidence and filename conflicts.
- Support efficient evidence searching and organization.
- Provide a simple interface for interacting with the evidence management system.

## ✨ Key Features

### 1. Cryptographic Fingerprinting
Uses the SHA-256 hashing algorithm to generate a fingerprint for each evidence file. Changes to the file content result in a different hash, helping identify modifications.

### 2. Merkle Tree Integrity Verification
Combines individual evidence hashes into a Merkle Tree and generates a Merkle Root representing the collection's integrity.

### 3. Evidence Tampering Detection
Recalculates evidence hashes and compares them with their originally stored fingerprints to identify possible tampering.

### 4. Duplicate Evidence Detection
Uses hash-based indexing to identify exact duplicate files, even when their filenames differ.

### 5. Filename Conflict Detection
Identifies conflicts when different file contents are submitted under an already-used filename.

### 6. Data Structures for Efficient Management
Uses data structures such as hash maps, lists, and tries to support evidence indexing, organization, and search operations.

### 7. Evidence Management Interface
Provides a web interface for interacting with the application and accessing supported evidence-management operations.

## 🛠️ Technologies Used

- **Python** — Core application logic
- **Flask** — Web application framework, if used by the current implementation
- **HTML, CSS, JavaScript** — Web interface
- **SHA-256** — Cryptographic hashing
- **Merkle Trees** — Integrity verification
- **Hash Maps and Tries** — Data organization and searching

## 📂 Project Structure

```text
MerkleVault/
├── README.md
├── requirements.txt
├── app.py
├── demo.py
├── dsa.py
└── static/
    └── index.html
```

| File or Folder | Description |
|---|---|
| `app.py` | Main application and server logic |
| `demo.py` | Demonstration of project functionality |
| `dsa.py` | Data structures and algorithms used in the project |
| `requirements.txt` | Python dependency list |
| `static/index.html` | Web interface |
| `README.md` | Project documentation |

## ⚙️ Installation and Setup

### Prerequisites

- Python 3 installed
- Git installed
- A terminal or command-line interface

### Step 1: Clone the Repository

```bash
git clone https://github.com/vadapallimouli/Smart_digital_evidence_vault.git
```

### Step 2: Navigate to the Project

```bash
cd Smart_digital_evidence_vault
```

If the project files are inside the `MerkleVault` subfolder, enter it:

```bash
cd MerkleVault
```

Run commands from the directory containing `app.py` and `requirements.txt`.

### Step 3: Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

For the web application:

```bash
python3 app.py
```

For the demonstration script:

```bash
python3 demo.py
```

Follow the terminal output to determine how to access the application.

> **Note:** The exact commands and available features depend on the current implementation of `app.py`, `demo.py`, and `requirements.txt`.

## 🔍 How It Works

1. **Evidence Input:** A digital evidence file is submitted to the system.
2. **Fingerprint Generation:** The system calculates the file's SHA-256 hash.
3. **Evidence Indexing:** The hash and associated evidence information are indexed.
4. **Duplicate Checking:** The system checks whether identical content already exists.
5. **Merkle Tree Construction:** Evidence hashes are combined to generate a Merkle Root.
6. **Integrity Verification:** The system recalculates hashes and compares them with the stored fingerprints.
7. **Tampering Detection:** A mismatch indicates that the evidence content may have changed.

## 🧮 Data Structures and Algorithms

| Technique | Purpose |
|---|---|
| SHA-256 hashing | Generates cryptographic fingerprints |
| Hash map | Supports fast hash-based lookups |
| Merkle Tree | Combines evidence hashes for integrity checking |
| Trie | Supports structured text or prefix-based searching |
| Lists and dictionaries | Store and organize evidence records |

## 🔒 Security and Limitations

- SHA-256 hashes help detect changes to file contents.
- A Merkle Root can help verify the integrity of a collection of evidence.
- A hash alone does not prove who created or submitted a file.
- A production digital forensics system would also need secure access controls, audit logs, protected hash storage, and appropriate evidence-handling procedures.
- The project is an academic prototype and should not be treated as a certified forensic evidence platform.

## 🚀 Future Enhancements

- Role-based access for investigators and administrators.
- Detailed evidence access and modification logs.
- Secure evidence backups and recovery.
- Advanced duplicate and modified-file analysis.
- Improved search and filtering.
- Case-wise evidence reports.
- Stronger authentication and evidence-chain-of-custody support.

## 🎓 Project Information

**Project Name:** MerkleVault — Smart Digital Evidence Management System  
**Domain:** Digital Forensics, Data Structures and Algorithms, and Data Integrity  
**Repository:** [Smart Digital Evidence Vault](https://github.com/vadapallimouli/Smart_digital_evidence_vault)

## 📜 License

This project is intended for academic and educational purposes. Add an appropriate open-source license if you intend to distribute or reuse the code publicly.
