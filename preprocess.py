import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def train_phish_shield():
    # --- PHASE 2 RECAP ---
    file_path = 'data/phishing_data.csv'
    df = pd.read_csv(file_path)

    features = ['URLLength', 'DomainLength', 'IsDomainIP', 'NoOfSubDomain', 
                'NoOfLettersInURL', 'NoOfDegitsInURL', 'NoOfEqualsInURL', 
                'NoOfQMarkInURL', 'NoOfAmpersandInURL', 'IsHTTPS']
    
    X = df[features]
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # --- PHASE 3: TRAINING ---
    print("Training the AI (Random Forest)... This may take a moment.")
    
    # Initialize the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Teach the model using the training data
    model.fit(X_train_scaled, y_train)
    
    # --- EVALUATION ---
    # Now quizzing the model on the 20% it hasn't seen yet
    predictions = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, predictions)
    
    print(f"\n Phase 3 Complete!")
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("\nDetailed Security Report:")
    print(classification_report(y_test, predictions))

if __name__ == "__main__":
    train_phish_shield()