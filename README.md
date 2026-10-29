# Customer Churn Prediction (Scikit-Learn · Pandas · Classification)

This project implements an end-to-end Machine Learning pipeline to predict customer churn in a telecommunications dataset, directly mirroring the following production resume bullet points:

> - Worked with a telecom dataset to predict churn from usage patterns, contract type, and billing info. Non-churners heavily outnumbered churners, so applied SMOTE to balance the classes, which improved minority-class performance noticeably.
> - Built Logistic Regression and Gradient Boosting models, then lowered the decision threshold after checking the precision-recall curve to improve churn detection.

---

## 📁 Project Structure

```
customer_churn_prediction/
│
├── Customer_Churn_Interview_Master_Guide.pdf  # 4-page comprehensive technical interview Q&A guide
├── customer-churn-rate.ipynb                 # Executed Jupyter Notebook with EDA, SMOTE, models, and PR curves
├── churn_pipeline.py                         # Standalone modular Python script for automated execution
├── requirements.txt                          # Python dependencies
└── README.md                                 # Detailed project documentation and interview talking points
```

---

## 🚀 Quickstart Guide

### 1. Set Up Virtual Environment & Install Dependencies
Open PowerShell or your preferred terminal in this directory:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Jupyter Notebook
Launch Jupyter:
```bash
jupyter notebook customer-churn-rate.ipynb
# or
jupyter lab
```
Run through each cell sequentially. All outputs, plots, and metrics will render interactively.

### 3. Run as a Standalone Script
You can also execute the entire pipeline with one command:
```bash
python churn_pipeline.py
```
This will train the models, output the classification metrics, and save evaluation plots (`churn_evaluation_plots.png`) to `./output/`.

---

## 🧠 Key Technical Highlights & Interview Defense

| Topic | Implementation Detail | Why It Matters |
| :--- | :--- | :--- |
| **Data Leakage Safeguard** | SMOTE is fitted **strictly on the training split** (`X_train`) after an 80/20 stratified train-test split. | Applying SMOTE across the whole dataset synthesizes points using test data, causing severe data leakage and artificially inflated metrics. |
| **Model Selection** | **Logistic Regression** (baseline) vs **Gradient Boosting Classifier** (final). | Logistic regression provides an interpretable linear baseline; Gradient boosting models non-linear interactions (e.g. Month-to-Month contracts combined with high monthly charges). |
| **Precision-Recall Curve** | Evaluated PR curve and PR-AUC instead of only ROC-AUC. | For imbalanced datasets (~73% non-churn vs ~27% churn), ROC-AUC can be deceptively high due to a huge True Negative denominator. PR curve focuses directly on minority-class precision and recall. |
| **Decision Threshold Tuning** | Lowered decision cutoff from default `0.50` to `0.35`. | In churn retention economics, **False Negatives** (missing a customer who leaves) cost hundreds of dollars in lifetime value, whereas **False Positives** only cost an email or promotion. Lowering the threshold captures significantly more churners (~80%+ Recall). |
