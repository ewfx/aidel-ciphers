# 🚀 RiskNova

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
A brief overview of your project and its purpose. Mention which problem statement are your attempting to solve. Keep it concise and engaging.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  

🖼️ Screenshots:

![Screenshot 1](./artifacts/arch/Screenshot_1.png)

![Screenshot 1](./artifacts/arch/Screenshot_2.png)

![Screenshot 1](./artifacts/arch/Screenshot_3.png)

## 💡 Inspiration
What inspired you to create this project? Describe the problem you're solving.

## ⚙️ What It Does
### Entity Extraction & Name Resolution
Feature: Extracts entity names from structured and unstructured transaction data.
Functionality: Uses Named Entity Recognition (NER) models to identify company names, people, and intermediaries. Handles name variations, abbreviations, and fuzzy matching to resolve inconsistencies.

### Data Enrichment & Verification
Feature: Enhances extracted entities with publicly available datasets.
Functionality:Integrates with APIs like OpenCorporates, Wikidata, SEC EDGAR, and OFAC Sanctions List.
Scrapes financial news and legal databases to gather additional risk indicators.

### Risk Classification & Anomaly Detection
Feature: Identifies fraudulent or high-risk entities based on known patterns.
Functionality:Implements Machine Learning models (Random Forest, XGBoost, or GNNs) for anomaly detection.
Flags shell companies, politically exposed persons (PEPs), and sanctioned entities.

### Risk Scoring Mechanism
Feature: Assigns a risk score (0 to 1) based on entity attributes and associated networks.
Functionality:Considers factors such as ownership structure, financial transactions, and past fraud history.Uses a weighted scoring system to prioritize risk levels.

### API & Output Format
Feature: Exposes an API endpoint for external integration.
Functionality:Provides responses in JSON/CSV format with extracted entities, risk scores, and supporting evidence.

## 🛠️ How We Built It
### Tech Stack & Frameworks
Programming Languages: Python (Backend & AI/ML), JavaScript (Frontend)
Machine Learning Frameworks: TensorFlow, PyTorch, Scikit-learn
Natural Language Processing: NLP

### Data Extraction & Processing
Libraries: pandas, NumPy, regex, PyTorch

### Entity Classification & Risk Scoring
Models Used: Random Forest, XGBoost, GNN (Graph Neural Networks) for anomaly detection

### Risk Scoring: Weighted algorithm combining entity type, ownership structure, past fraud records, and financial behavior

## 🚧 Challenges We Faced
### Data Enrichment & API Rate Limits
Implemented caching mechanisms and parallel API requests to optimize data retrieval.

### Generating Explainable Risk Scores
AI models provided risk scores, but lacked interpretability for analysts.
LLM-powered textual justifications to enhance transparency.

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/ewfx/aidel-ciphers.git
   ```
2. Install dependencies  
   ```sh
   pip install -r requirements.txt (for Python)
   ```
3. Run the project  
   ```sh
   python app.py
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: React 
- 🔹 Backend: Flask / Python
- 🔹 Other: PyTorch API / Pandas / Numpy

## 👥 Team
- **Ashritha Nagandla** - [GitHub](https://github.com/Ashritha-01) | [LinkedIn](#)
- **Hyma Lakshmi Nelluri** - [GitHub](https://github.com/hyma09) | [LinkedIn](#)
- **Tamojit Das** - [GitHub](https://github.com/tamojit2000) | [LinkedIn](https://www.linkedin.com/in/tamojit-das-ab425b228/)
