"""
AgriSense - Machine Learning Model Training & Evaluation Pipeline
Trains and rigorously compares 5 classification models on the verified dataset:
- Random Forest Classifier
- Decision Tree Classifier
- K-Nearest Neighbors (with StandardScaler)
- Support Vector Machine (RBF kernel, with StandardScaler)
- Gaussian Naive Bayes

Computes actual multiclass evaluation metrics:
- Accuracy, Precision (weighted & macro), Recall (weighted & macro), F1-Score (weighted & macro)
- Confusion Matrix for all 22 crop classes
- Saves best model to saved_models/crop_recommendation_model.joblib
- Saves detailed metrics to saved_models/ml_metrics.json
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

def train_and_evaluate_models(data_path="data/processed/crop_recommendation_clean.csv", output_dir="saved_models"):
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Clean dataset not found at {data_path}. Run data preparation first.")

    df = pd.read_csv(data_path)
    feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    target_col = 'label'

    X = df[feature_cols]
    y = df[target_col]

    classes = sorted(y.unique().tolist())

    # Reproducible stratified split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    models = {
        "Random Forest": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", RandomForestClassifier(n_estimators=100, random_state=42, max_depth=15))
        ]),
        "Decision Tree": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", DecisionTreeClassifier(random_state=42, max_depth=15))
        ]),
        "K-Nearest Neighbors": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", KNeighborsClassifier(n_neighbors=5))
        ]),
        "Support Vector Machine": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", SVC(kernel='rbf', probability=True, random_state=42, C=10.0))
        ]),
        "Gaussian Naive Bayes": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", GaussianNB())
        ])
    }

    results = {}
    best_model_name = None
    best_f1 = -1.0
    best_pipeline = None

    print(f"Dataset split: {len(X_train)} training samples, {len(X_test)} testing samples across {len(classes)} classes.")

    for name, pipeline in models.items():
        print(f"Training {name}...")
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        acc = float(accuracy_score(y_test, y_pred))
        p_weighted = float(precision_score(y_test, y_pred, average='weighted', zero_division=0))
        r_weighted = float(recall_score(y_test, y_pred, average='weighted', zero_division=0))
        f1_weighted = float(f1_score(y_test, y_pred, average='weighted', zero_division=0))

        p_macro = float(precision_score(y_test, y_pred, average='macro', zero_division=0))
        r_macro = float(recall_score(y_test, y_pred, average='macro', zero_division=0))
        f1_macro = float(f1_score(y_test, y_pred, average='macro', zero_division=0))

        cm = confusion_matrix(y_test, y_pred, labels=classes).tolist()
        clf_rep = classification_report(y_test, y_pred, labels=classes, output_dict=True, zero_division=0)

        results[name] = {
            "accuracy": round(acc, 4),
            "precision_weighted": round(p_weighted, 4),
            "recall_weighted": round(r_weighted, 4),
            "f1_weighted": round(f1_weighted, 4),
            "precision_macro": round(p_macro, 4),
            "recall_macro": round(r_macro, 4),
            "f1_macro": round(f1_macro, 4),
            "confusion_matrix": cm,
            "classification_report": clf_rep
        }

        print(f"-> {name} Results: Acc={acc:.4f}, F1-Weighted={f1_weighted:.4f}")

        if f1_weighted > best_f1:
            best_f1 = f1_weighted
            best_model_name = name
            best_pipeline = pipeline

    print(f"\nBest Model Selected: {best_model_name} with F1-Weighted: {best_f1:.4f}")

    # Save best model
    model_save_path = os.path.join(output_dir, "crop_recommendation_model.joblib")
    joblib.dump({
        "pipeline": best_pipeline,
        "model_name": best_model_name,
        "classes": classes,
        "features": feature_cols,
        "train_samples": len(X_train),
        "test_samples": len(X_test)
    }, model_save_path)
    print(f"Saved best model pipeline to {model_save_path}")

    # Prepare ML Dashboard metrics metadata
    metrics_summary = {
        "dataset_info": {
            "name": "Crop Recommendation Dataset",
            "source": "Atharva Ingle (Kaggle public dataset)",
            "total_samples": int(len(df)),
            "train_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
            "features": feature_cols,
            "num_features": len(feature_cols),
            "num_classes": len(classes),
            "classes": classes
        },
        "selected_model": best_model_name,
        "models_comparison": [
            {
                "model_name": m_name,
                "accuracy": m_data["accuracy"],
                "precision": m_data["precision_weighted"],
                "recall": m_data["recall_weighted"],
                "f1_score": m_data["f1_weighted"],
                "is_selected": (m_name == best_model_name)
            }
            for m_name, m_data in results.items()
        ],
        "detailed_results": results
    }

    metrics_path = os.path.join(output_dir, "ml_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics_summary, f, indent=2)
    print(f"Saved evaluation metrics to {metrics_path}")

    return metrics_summary

if __name__ == "__main__":
    train_and_evaluate_models()
