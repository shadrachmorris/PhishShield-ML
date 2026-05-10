import streamlit as st
import pandas as pd
import joblib
import re
from urllib.parse import urlparse

# --- Page Config ---
st.set_page_config(page_title="PhishShield-ML", page_icon="🛡️", layout="wide")

# --- Load the AI Brain ---
@st.cache_resource
def load_ai():
    # Ensure these files are in main folder on GitHub
    model = joblib.load('phish_model.pkl')
    scaler = joblib.load('scaler.pkl')
    return model, scaler

model, scaler = load_ai()

# --- Feature Extraction Logic ---
def extract_features(url):
    parsed = urlparse(url)
    host = parsed.netloc
    url_len = len(url)
    domain_len = len(host)
    is_ip = 1 if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host) else 0
    subdomains = host.count('.')
    is_https = 1 if parsed.scheme == 'https' else 0
    digits = sum(c.isdigit() for c in url)
    letters = sum(c.isalpha() for c in url)
    # Match the 10 features from training
    return [url_len, domain_len, is_ip, subdomains, letters, digits, 
            url.count('='), url.count('?'), url.count('&'), is_https]

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["About PhishShield", "Live AI Scanner"])

# --- PAGE 1: DESCRIPTION ---
if page == "About PhishShield":
    st.title("🛡️ Project Overview: PhishShield-ML")
    st.markdown("""
    ### The Mission
    PhishShield-ML is a high-performance security tool designed to identify malicious URLs before they can compromise a system. 
    By analyzing the structural DNA of a link, the AI can detect patterns that are invisible to the human eye.

    ### Technical Specifications
    * **Core Model:** Random Forest Classifier (100 Decision Trees).
    * **Dataset:** PhiUSIIL 2024 (Training set of 188,000+ samples).
    * **Verified Accuracy:** **99.76%**.
    * **Feature Engineering:** 10 structural features normalized via `StandardScaler`.

    ### How It Works
    When you paste a link into the scanner, the system performs a **Digital Autopsy**:
    1. **Parsing:** Breaks the string into scheme, host, and path.
    2. **Extraction:** Counts subdomains, digits, and special characters.
    3. **Scaling:** Shrunks raw numbers down to a -1 to 1 range so the AI can read them fairly.
    4. **Inference:** The "Brain" votes on the threat level.
    """)
    st.info("Developed by Shadrach Morris | University of North Texas")

# --- PAGE 2: THE WORK ---
elif page == "Live AI Scanner":
    st.title("🔍 Live Threat Analysis")
    st.write("Paste a URL below to see the AI analyze it in real-time.")

    user_url = st.text_input("URL to Scan:", placeholder="https://example-secure-login.com")

    if st.button("Run AI Analysis"):
        if user_url:
            with st.spinner("Analyzing structural patterns..."):
                # Run the math
                features = extract_features(user_url)
                scaled_input = scaler.transform([features])
                prediction = model.predict(scaled_input)
                
                st.divider()
                if prediction[0] == 1:
                    st.error(f"### ⚠️ THREAT DETECTED")
                    st.write(f"The URL **{user_url}** matches known phishing signatures.")
                else:
                    st.success(f"### ✅ URL SECURE")
                    st.write(f"The structural analysis suggests this link is legitimate.")
                
                # Show the 'Numbers' to the user for transparency
                with st.expander("View Raw Feature Data"):
                    st.write(pd.DataFrame([features], columns=[
                        "URL Len", "Domain Len", "IP Addr", "Subdomains", 
                        "Letters", "Digits", "Equals", "QMark", "Amp", "HTTPS"
                    ]))
        else:
            st.warning("Please enter a URL to continue.")