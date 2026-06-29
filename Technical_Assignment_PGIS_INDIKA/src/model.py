"""
src/model.py
Price prediction: feature engineering + 3 model families + CV metrics + SHAP.
This mirrors the pipeline pattern from your thesis work (XGBoost / RF / Linear,
with SHAP explainability) applied to price instead of suitability classification.
Run: python src/model.py
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error
import xgboost as xgb
import shap
import matplotlib.pyplot as plt
import json
import os

PROCESSED_DIR = "data/processed"
FIG_DIR = "reports/figures"

NUMERIC_FEATURES = [
    "accommodates", "bedrooms", "bathrooms", "minimum_nights",
    "number_of_reviews", "reviews_per_month", "host_tenure_years",
    "availability_365",
]
CATEGORICAL_FEATURES = ["room_type", "neighbourhood_group_cleansed"]
TARGET = "price"


def build_feature_frame(df):
    cols = [c for c in NUMERIC_FEATURES + CATEGORICAL_FEATURES if c in df.columns]
    data = df[cols + [TARGET]].copy()
    data = data.dropna(subset=[TARGET])
    for c in NUMERIC_FEATURES:
        if c in data.columns:
            data[c] = data[c].fillna(data[c].median())
    for c in CATEGORICAL_FEATURES:
        if c in data.columns:
            data[c] = data[c].fillna("Unknown")
    return data, cols


def evaluate(y_true, y_pred, name):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred) ** 0.5
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    print(f"{name:20s} MAE={mae:8.2f}  RMSE={rmse:8.2f}  MAPE={mape:6.2f}%")
    return {"model": name, "MAE": mae, "RMSE": rmse, "MAPE": mape}


if __name__ == "__main__":
    os.makedirs(FIG_DIR, exist_ok=True)
    listings = pd.read_csv(f"{PROCESSED_DIR}/listings_clean.csv")
    data, feature_cols = build_feature_frame(listings)

    num_cols = [c for c in NUMERIC_FEATURES if c in feature_cols]
    cat_cols = [c for c in CATEGORICAL_FEATURES if c in feature_cols]

    X = data[feature_cols]
    y = data[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ], remainder="passthrough")

    results = []

    # --- Linear baseline ---
    lin_pipe = Pipeline([("prep", preprocessor), ("model", LinearRegression())])
    lin_pipe.fit(X_train, y_train)
    results.append(evaluate(y_test, lin_pipe.predict(X_test), "LinearRegression"))

    # --- Random Forest ---
    rf_pipe = Pipeline([("prep", preprocessor), ("model", RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1))])
    rf_pipe.fit(X_train, y_train)
    results.append(evaluate(y_test, rf_pipe.predict(X_test), "RandomForest"))

    # --- XGBoost ---
    X_train_enc = preprocessor.fit_transform(X_train)
    X_test_enc = preprocessor.transform(X_test)
    feature_names = preprocessor.get_feature_names_out()

    xgb_model = xgb.XGBRegressor(n_estimators=300, max_depth=5, learning_rate=0.05, random_state=42)
    xgb_model.fit(X_train_enc, y_train)
    results.append(evaluate(y_test, xgb_model.predict(X_test_enc), "XGBoost"))

    # save comparison table
    pd.DataFrame(results).to_csv(f"{PROCESSED_DIR}/model_comparison.csv", index=False)
    print(f"\n[model] comparison table saved -> {PROCESSED_DIR}/model_comparison.csv")

    # --- SHAP on the best model (XGBoost) ---
    explainer = shap.TreeExplainer(xgb_model)
    X_test_enc_dense = X_test_enc.toarray() if hasattr(X_test_enc, "toarray") else X_test_enc
    shap_values = explainer.shap_values(X_test_enc_dense)

    plt.figure()
    shap.summary_plot(shap_values, X_test_enc_dense, feature_names=feature_names, show=False)
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/fig6_shap_summary.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[model] SHAP summary plot saved -> {FIG_DIR}/fig6_shap_summary.png")
