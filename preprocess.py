import pandas as pd
import os

def load_data():
    # Double check the path
    file_path = 'data/phishing_data.csv'
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at {file_path}")
        print("Check if you unzipped the file in the data folder!")
        return

    try:
        # Pulling the first 5 rows to check headers
        df = pd.read_csv(file_path, nrows=5)
        print("✅ Success! Dataset connected.")
        print("\nColumn names found in this dataset:")
        print(df.columns.tolist())
    except Exception as e:
        print(f"❌ Error reading the CSV: {e}")
        
if __name__ == "__main__":
    load_data()