# 🔐 Smart Digital Evidence Management Using Merkle Tree and AI (MerkleVault)

**Team A-9 | Final Project Review**

## 👥 Team Members

| S. No. | Name | Register Number |
|---|---|---|
| 1 | H. Bala Sri Siva Sai Surya Teja | CB.AI.U4AID25017 |
| 2 | V. Mouli Sri | CB.AI.U4AID25066 |
| 3 | B. Sharmitha | CB.AI.U4AID25007 |
| 4 | C. Jasmitha | CB.AI.U4AID25011 |

**Department:** B.Tech Artificial Intelligence & Data Science  
**Institution:** Amrita Vishwa Vidyapeetham, Coimbatore  

---

## 📌 About the Project

**MerkleVault** is a web-based digital evidence management system designed to organize digital evidence and support evidence integrity verification.

The system combines cryptographic hashing, Merkle Tree verification, content-based tamper detection, duplicate detection, intelligent searching, and investigation management workflows.

## 🎯 Objectives

- Securely manage digital evidence.
- Generate SHA-256 fingerprints for uploaded files.
- Verify evidence integrity using Merkle Trees.
- Detect duplicate evidence and potential content modifications.
- Identify filename conflicts.
- Organize evidence through automatic classification and Trie-based searching.
- Maintain evidence records and chain-of-custody information.
- Support departmental dashboards, investigation reports, and approval workflows.

## ✨ Key Features

### 🔐 1. Evidence Integrity Verification
Uses SHA-256 fingerprints and Merkle Tree concepts to support the verification of evidence integrity.

### 🔍 2. Content-Based Tamper Detection
Compares evidence content to identify potential modifications according to the implemented comparison criteria.

### 🧬 3. Duplicate Evidence Detection
Identifies identical file content, even when files have different names.

### ⚠️ 4. Filename Conflict Detection
Detects when different content is uploaded using an existing filename.

### 🗂️ 5. Intelligent Evidence Organization
Supports Trie-based prefix searching and automatic classification of supported files.

### 🏛️ 6. Department and Authority Management
Organizes investigation activities through department-specific dashboards and hierarchical access workflows.

### 📑 7. Report Management
Supports investigation reports, review and approval workflows, chain-of-custody records, and digital signing features.

## 🛠️ Technologies and Concepts

- **HTML5** — Web page structure.
- **CSS3** — User interface styling.
- **JavaScript** — Client-side functionality.
- **SHA-256** — Cryptographic file fingerprinting.
- **Merkle Tree** — Hierarchical hash-based integrity verification.
- **Hash Map** — Efficient fingerprint lookup.
- **Trie** — Prefix-based searching.
- **Content Comparison** — Identification of content similarities and changes.

*The technologies and features listed above should match the actual implementation in the repository.*

## 📂 Project Structure

```text
Smart-Digital-Evidence-Management/
│
├── Smart_digital_evidence_vault.html
└── README.md
```

If you rename the HTML file to `index.html` for GitHub Pages, update the filename accordingly.

## 🚀 How to Run the Project

1. Clone or download this repository.
2. Open the project folder.
3. Open `Smart_digital_evidence_vault.html` in a modern web browser.
4. Explore the available evidence management and verification features.

No separate development server is required to open a standalone HTML file.

## 🌐 Deployment Using GitHub Pages

1. Upload the project files to your GitHub repository.
2. Rename the main HTML file to `index.html` if needed.
3. Open your repository's **Settings**.
4. Select **Pages**.
5. Configure deployment from the `main` branch and the root folder.
6. Save the settings and wait for deployment.
7. Open the website URL displayed in the Pages section.

## 🔒 Security Considerations

This project is developed for academic and demonstration purposes.

- Client-side functionality alone does not guarantee secure evidence storage.
- Data held only in browser memory may be lost when the page is refreshed or closed.
- SHA-256 fingerprints help identify exact content changes, while partial-content similarity requires separate comparison logic.
- Production deployment would require secure backend storage, authentication, access controls, audit logging, and verified chain-of-custody mechanisms.

**Do not upload real or confidential digital evidence to a public repository.**

## 🔮 Future Enhancements

- Advanced content-similarity analysis.
- Testing with larger evidence datasets.
- Support for additional digital evidence formats.
- Improved evidence retrieval efficiency.
- Stronger audit logging and investigation analytics.
- Enhanced secure storage and access management.

## 🎓 Academic Project

This project was developed as part of the **B.Tech Artificial Intelligence & Data Science** program at **Amrita Vishwa Vidyapeetham, Coimbatore**.

**Project Title:** Smart Digital Evidence Management Using Merkle Tree and AI  
**Project Name:** MerkleVault  
**Team:** A-9

---

## 📄 License

No license has been specified. Add an appropriate open-source license if you intend to allow others to reuse or modify this project.
