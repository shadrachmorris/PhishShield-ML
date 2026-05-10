# 🛡️ PhishShield-ML

An AI-powered cybersecurity tool designed to detect phishing URLs and social engineering tactics with **99.76% accuracy**.

## 🔗 Live Application
**Check out the live app here:** https://phishshield-ml.streamlit.app
---

## 🚀 Technical Highlights
* **Machine Learning Architecture:** Utilizes a **Random Forest Classifier** trained on structural URL metadata to identify malicious patterns.
* **Automated Feature Engineering:** Custom **Python/Regex** pipeline that extracts 10 critical data points (length, digits, subdomains, etc.) from raw strings for real-time inference.
* **Email Security Guard:** Includes a hybrid analysis engine that scans email bodies for high-pressure social engineering keywords and embedded malicious links.
* **Cloud Deployment:** Fully responsive **Streamlit** web application deployed for cross-platform use on iOS, Android, and Desktop.

## 🛠️ Tech Stack
* **Languages:** Python (Regex, Urllib, Pandas)
* **AI/ML:** Scikit-Learn, Joblib, NumPy
* **Frontend:** Streamlit (Custom CSS & UI/UX)
* **DevOps:** GitHub, Streamlit Cloud, Git

## 📂 Project Structure
```text
├── web_app.py          # Main Streamlit UI and logic
├── phish_model.pkl      # Trained Random Forest brain
├── scaler.pkl           # Pre-fitted StandardScaler for inputs
├── requirements.txt     # Server-side dependencies (Joblib, Scikit-Learn, etc.)
└── README.md            # Project documentation
