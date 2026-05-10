import streamlit as st
import pandas as pd
import joblib
import re
from urllib.parse import urlparse

# --- Page Config & Styling ---
st.set_page_config(page_title="PhishShield-ML", page_icon="🛡️", layout="wide")

# Custom CSS for the look
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #4A90E2;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 15px;
    }
    .status-box {
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Load the AI Brain ---
@st.cache_resource
def load_ai():
    model = joblib.load('phish_model.pkl')
    scaler = joblib.load('scaler.pkl')
    return model, scaler

model, scaler = load_ai()

# --- Shared Logic ---
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
    return [url_len, domain_len, is_ip, subdomains, letters, digits, 
            url.count('='), url.count('?'), url.count('&'), is_https]

# --- Sidebar Navigation ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
    st.title("PhishShield Hub")
    page = st.radio("Navigation", ["🏠 Home / About", "🔍 URL Scanner", "📧 Email Guard"])
    st.divider()
    st.caption("Version 1.1 | Developed by Shadrach Morris")

# --- PAGE 1: HOME ---
if page == "🏠 Home / About":
    st.title("🛡️ PhishShield-ML")
    st.subheader("Next-Generation Defensive Intelligence")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Why PhishShield?
        Traditional blacklists can't keep up with new threats. **PhishShield-ML** uses a 
        **Random Forest Architecture** to analyze the structural DNA of a link, 
        detecting malicious intent with **99.76% accuracy** before the first click.
        
        #### Core Pillars:
        * **Structural Analysis:** We don't just look at the name; we look at the math.
        * **Behavioral Heuristics:** Identifying social engineering tactics in text.
        * **Real-time Inference:** Decisions made in milliseconds.
        """)
    with col2:
        st.metric(label="Model Accuracy", value="99.76%")
        st.metric(label="Threat Vector Analysis", value="10 Features")

# --- PAGE 2: SCANNER ---
elif page == "🔍 URL Scanner":
    st.title("🔍 Real-Time URL Analysis")
    
    with st.container():
        st.write("Enter a link below to perform a forensic structural scan.")
        user_url = st.text_input("Target URL:", placeholder="https://secure-login-bank.com")
        
        if st.button("Initiate Scan"):
            if user_url:
                with st.spinner("Decoding URL structure..."):
                    features = extract_features(user_url)
                    scaled_input = scaler.transform([features])
                    prediction = model.predict(scaled_input)
                    
                    if prediction[0] == 1:
                        st.error("### 🚨 HIGH RISK DETECTED")
                        st.write("This URL demonstrates structural patterns common in phishing attacks.")
                    else:
                        st.success("### ✅ CLEARANCE GRANTED")
                        st.write("Structural markers suggest this URL is legitimate.")
            else:
                st.warning("Please provide a URL to analyze.")

# --- PAGE 3: EMAIL GUARD ---
elif page == "📧 Email Guard":
    st.title("📧 Email Social Engineering Guard")
    st.write("Paste suspicious email content to scan for hidden threats.")
    
    email_body = st.text_area("Email Body Content:", height=250)
    
    if st.button("Run Threat Assessment"):
        if email_body:
            urls = re.findall(r'(https?://\S+)', email_body)
            urgency_keywords = ['urgent', 'suspend', 'immediate', 'action required', 'penalty', 'verify']
            found_keywords = [w for w in urgency_keywords if w in email_body.lower()]
            
            c1, c2 = st.columns(2)
            with c1:
                st.info("#### Language Analysis")
                if found_keywords:
                    st.warning(f"Social Engineering Flags: {', '.join(found_keywords)}")
                else:
                    st.success("No high-pressure language patterns found.")
            
            with c2:
                st.info("#### Embedded Link Analysis")
                if urls:
                    for u in urls:
                        f = extract_features(u)
                        res = model.predict(scaler.transform([f]))
                        if res[0] == 1:
                            st.error(f"Malicious: {u[:30]}...")
                        else:
                            st.success(f"Safe: {u[:30]}...")
                else:
                    st.write("No external links detected.")