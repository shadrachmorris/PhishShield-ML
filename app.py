import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

# --- Step 1: Load the Saved "Brain" ---
# (Will update preprocess.py to save this file in a second)
def predict_url(url_features):
    try:
        model = joblib.load('phish_model.pkl')
        scaler = joblib.load('scaler.pkl')
        
        # Scale the input features exactly like we did in training
        scaled_features = scaler.transform([url_features])
        
        prediction = model.predict(scaled_features)
        return "⚠️ PHISHING DETECTED" if prediction[0] == 1 else "✅ SAFE URL"
    except:
        return "Model files not found. Run preprocess.py first!"

# --- Step 2: Live Test ---
if __name__ == "__main__":
    print("--- PhishShield-ML Live Scanner ---")
    
    # Get user input for a simple test
    length = int(input("Enter URL Length: "))
    https = int(input("Is it HTTPS? (1 for Yes, 0 for No): "))
    
    # Create a test link using your input + some default 'safe' values for others
    # [URLLength, DomainLength, IsDomainIP, NoOfSubDomain, NoOfLetters, NoOfDigits, Equals, QMark, Ampersand, IsHTTPS]
    user_test = [length, 30, 0, 1, length-10, 5, 0, 0, 0, https]
    
    print(f"\nScanning...")
    print(f"Result: {predict_url(user_test)}")