"""
Train a Random Forest model for disease risk prediction.
Uses the UCI Heart Disease dataset.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "disease_model.pkl")

# UCI Heart Disease dataset features
FEATURES = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal"
]

def load_heart_disease_data():
    """Load UCI Heart Disease dataset from online source."""
    try:
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
        df = pd.read_csv(url, header=None, na_values="?")
        
        # Column names for the Cleveland dataset
        column_names = [
            "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
            "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"
        ]
        df.columns = column_names
        
        # Remove rows with missing values
        df = df.dropna()
        
        # Convert target to binary (0 = no disease, 1 = disease present)
        df["target"] = (df["target"] > 0).astype(int)
        
        print(f"✓ Loaded UCI Heart Disease dataset: {len(df)} samples")
        return df
    except Exception as e:
        print(f"✗ Failed to load UCI dataset: {e}")
        return None

def generate_synthetic_data():
    """Generate synthetic heart disease data for demonstration."""
    np.random.seed(42)
    n_samples = 500
    
    data = {
        "age": np.random.randint(28, 78, n_samples),
        "sex": np.random.randint(0, 2, n_samples),
        "cp": np.random.randint(1, 5, n_samples),
        "trestbps": np.random.randint(90, 200, n_samples),
        "chol": np.random.randint(126, 570, n_samples),
        "fbs": np.random.randint(0, 2, n_samples),
        "restecg": np.random.randint(0, 3, n_samples),
        "thalach": np.random.randint(71, 202, n_samples),
        "exang": np.random.randint(0, 2, n_samples),
        "oldpeak": np.random.uniform(0, 6.2, n_samples),
        "slope": np.random.randint(1, 4, n_samples),
        "ca": np.random.randint(0, 4, n_samples),
        "thal": np.random.choice([3, 6, 7], n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create target variable with some correlation to features
    target = (
        (df["age"] > 55).astype(int) * 0.3 +
        (df["chol"] > 240).astype(int) * 0.25 +
        (df["trestbps"] > 140).astype(int) * 0.2 +
        (df["thalach"] < 100).astype(int) * 0.15 +
        (df["exang"] == 1).astype(int) * 0.1 > 0.5
    ).astype(int)
    
    df["target"] = target
    print(f"✓ Generated synthetic dataset: {len(df)} samples")
    return df

def train_and_save_model():
    """Train Random Forest model and save it."""
    print("Training disease risk prediction model...")
    
    # Try to load real data, fall back to synthetic
    df = load_heart_disease_data()
    if df is None:
        print("Using synthetic data for demonstration...")
        df = generate_synthetic_data()
    
    # Prepare features and target
    X = df[FEATURES]
    y = df["target"]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    print("Training Random Forest classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    print(f"✓ Training accuracy: {train_score:.4f}")
    print(f"✓ Testing accuracy: {test_score:.4f}")
    
    # Save model
    joblib.dump(model, MODEL_PATH)
    print(f"✓ Model saved to: {MODEL_PATH}")
    
    # Feature importance
    print("\nTop 5 important features:")
    importance_df = pd.DataFrame({
        "feature": FEATURES,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)
    
    for idx, row in importance_df.head(5).iterrows():
        print(f"  {row['feature']}: {row['importance']:.4f}")

if __name__ == "__main__":
    try:
        train_and_save_model()
        print("\n✓ Model training complete!")
    except Exception as e:
        print(f"\n✗ Error during training: {e}")
        import traceback
        traceback.print_exc()
