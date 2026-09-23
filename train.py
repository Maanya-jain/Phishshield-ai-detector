import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from features import extract_features_from_url

CSV_PATH = 'archive/MUD_malicious_urls_2026_V2.csv'

def main():
    print("Loading dataset with larger sample...")
    df = pd.read_csv(CSV_PATH, nrows=120000, usecols=['url', 'label'])
    df = df.dropna()

    # 0 = Safe, 1 = Suspicious
    df['target'] = df['label'].apply(lambda x: 0 if str(x).strip().lower() in ['0', 'benign', 'good'] else 1)

    urls = df['url'].values
    y = df['target'].values

    print(f"Extracting enhanced features from {len(urls)} URLs...")
    X = np.array([extract_features_from_url(u) for u in urls])

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training tuned Random Forest (approx 40-50 seconds)...")
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=20,
        min_samples_split=4,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    print("\n--- New Model Evaluation ---")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"New Model Accuracy: {acc * 100:.2f}%\n")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, 'phishing_model.pkl')
    print("Success: Updated 'phishing_model.pkl' successfully save ho gaya!")

if __name__ == '__main__':
    main()