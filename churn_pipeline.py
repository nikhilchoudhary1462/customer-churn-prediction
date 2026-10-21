"""
Customer Churn Prediction Pipeline
Tech stack: Python, Pandas, Scikit-Learn, Imbalanced-Learn

Key features implemented:
- Preprocessing with ColumnTransformer (OneHotEncoder + StandardScaler)
- Stratified Train-Test Split to preserve churn proportion
- SMOTE oversampling applied ONLY to the training set (preventing data leakage)
- Logistic Regression (interpretable linear baseline)
- Gradient Boosting Classifier (handles complex non-linear interactions)
- Precision-Recall Curve analysis & Decision Threshold Tuning
- Feature Importance extraction
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_recall_curve,
    roc_auc_score,
    average_precision_score,
    f1_score,
    recall_score,
    precision_score
)
from imblearn.over_sampling import SMOTE


def load_and_clean_data(dataset_url=None):
    if dataset_url is None:
        dataset_url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-premise/master/data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    
    print(f"[+] Loading dataset from: {dataset_url}")
    df = pd.read_csv(dataset_url)
    
    # Drop identifier
    if "customerID" in df.columns:
        df = df.drop(columns=["customerID"])
        
    # 'TotalCharges' contains whitespace strings for brand new customers (tenure = 0)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"].str.strip(), errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(0)
    
    # Encode target
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    
    churn_rate = df["Churn"].mean() * 100
    print(f"[✓] Data loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
    print(f"    Churn rate: {churn_rate:.2f}% (Non-churn: {100 - churn_rate:.2f}%)")
    
    return df


def build_pipeline_and_evaluate(df, output_dir="./output"):
    os.makedirs(output_dir, exist_ok=True)
    
    X = df.drop(columns=["Churn"])
    y = df["Churn"]
    
    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
    numerical_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    
    print(f"[+] Features: {len(numerical_cols)} numerical, {len(categorical_cols)} categorical.")
    
    # 1. Stratified Train-Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    # 2. Preprocessor (Fit ONLY on train set)
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_cols),
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), categorical_cols),
        ]
    )
    
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)
    
    # Extract encoded feature names for feature importance
    cat_encoder = preprocessor.named_transformers_["cat"]
    encoded_cat_names = cat_encoder.get_feature_names_out(categorical_cols).tolist()
    all_feature_names = numerical_cols + encoded_cat_names
    
    # 3. Apply SMOTE to Training Set ONLY
    print(f"\n[+] Applying SMOTE on training data...")
    print(f"    Before SMOTE: Non-Churn = {(y_train == 0).sum()}, Churn = {(y_train == 1).sum()}")
    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train_proc, y_train)
    print(f"    After SMOTE:  Non-Churn = {(y_train_smote == 0).sum()}, Churn = {(y_train_smote == 1).sum()}")
    
    # 4. Model Training
    print("\n[+] Training Logistic Regression...")
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train_smote, y_train_smote)
    
    print("[+] Training Gradient Boosting Classifier...")
    gb = GradientBoostingClassifier(n_estimators=150, learning_rate=0.08, max_depth=3, random_state=42)
    gb.fit(X_train_smote, y_train_smote)
    
    # 5. Baseline Evaluation (Standard threshold 0.50)
    y_probs_lr = lr.predict_proba(X_test_proc)[:, 1]
    y_probs_gb = gb.predict_proba(X_test_proc)[:, 1]
    
    print("\n" + "="*50)
    print(" BASELINE MODEL COMPARISON (Threshold = 0.50)")
    print("="*50)
    print(f"Logistic Regression ROC-AUC: {roc_auc_score(y_test, y_probs_lr):.4f}")
    print(f"Logistic Regression PR-AUC:  {average_precision_score(y_test, y_probs_lr):.4f}")
    print(f"Gradient Boosting   ROC-AUC: {roc_auc_score(y_test, y_probs_gb):.4f}")
    print(f"Gradient Boosting   PR-AUC:  {average_precision_score(y_test, y_probs_gb):.4f}")
    
    # 6. Precision-Recall Curve & Threshold Tuning on Gradient Boosting
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_probs_gb)
    
    # Compute F1 across thresholds
    f1_scores = 2 * (precisions[:-1] * recalls[:-1]) / (precisions[:-1] + recalls[:-1] + 1e-10)
    best_idx = np.argmax(f1_scores)
    best_thresh_f1 = thresholds[best_idx]
    
    # Select business-oriented lowered threshold (e.g. 0.35 to catch higher recall)
    lowered_thresh = 0.35
    
    y_pred_gb_default = (y_probs_gb >= 0.50).astype(int)
    y_pred_gb_tuned = (y_probs_gb >= lowered_thresh).astype(int)
    
    print("\n" + "="*50)
    print(" THRESHOLD TUNING COMPARISON (Gradient Boosting)")
    print("="*50)
    print("\n[Default Threshold: 0.50]")
    print(classification_report(y_test, y_pred_gb_default, target_names=["Stay", "Churn"]))
    
    print(f"\n[Lowered Decision Threshold: {lowered_thresh:.2f}] (Higher Recall for Churners)")
    print(classification_report(y_test, y_pred_gb_tuned, target_names=["Stay", "Churn"]))
    
    # 7. Visualization: Precision-Recall Curve & Feature Importance
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot PR Curve
    axes[0].plot(recalls, precisions, label=f"PR Curve (PR-AUC = {average_precision_score(y_test, y_probs_gb):.3f})", color="navy", lw=2)
    axes[0].scatter(
        recall_score(y_test, y_pred_gb_default),
        precision_score(y_test, y_pred_gb_default),
        marker="o", color="red", s=90, label=f"Default Thresh (0.50) [Recall={recall_score(y_test, y_pred_gb_default):.2f}]"
    )
    axes[0].scatter(
        recall_score(y_test, y_pred_gb_tuned),
        precision_score(y_test, y_pred_gb_tuned),
        marker="^", color="green", s=110, label=f"Lowered Thresh ({lowered_thresh:.2f}) [Recall={recall_score(y_test, y_pred_gb_tuned):.2f}]"
    )
    axes[0].set_title("Precision-Recall Curve & Threshold Trade-off", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Recall (Coverage of Churners)", fontsize=11)
    axes[0].set_ylabel("Precision (Accuracy of Churn Alarms)", fontsize=11)
    axes[0].legend(loc="lower left")
    axes[0].grid(True, linestyle="--", alpha=0.5)
    
    # Plot Top 10 Feature Importances
    importances = gb.feature_importances_
    top_indices = np.argsort(importances)[-10:]
    top_features = [all_feature_names[i] for i in top_indices]
    top_scores = importances[top_indices]
    
    axes[1].barh(top_features, top_scores, color="teal")
    axes[1].set_title("Top 10 Feature Importances (Gradient Boosting)", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Relative Importance Score", fontsize=11)
    axes[1].grid(axis="x", linestyle="--", alpha=0.5)
    
    plt.tight_layout()
    plot_path = os.path.join(output_dir, "churn_evaluation_plots.png")
    plt.savefig(plot_path, dpi=300)
    print(f"\n[✓] Evaluation plots saved to: {plot_path}")
    
    return {
        "gb_model": gb,
        "lr_model": lr,
        "preprocessor": preprocessor,
        "default_threshold": 0.50,
        "lowered_threshold": lowered_thresh,
        "best_f1_threshold": best_thresh_f1
    }


if __name__ == "__main__":
    df = load_and_clean_data()
    build_pipeline_and_evaluate(df)
