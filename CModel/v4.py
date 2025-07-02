import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, RocCurveDisplay
from lightgbm import LGBMClassifier
from imblearn.over_sampling import SMOTE
import shap
import matplotlib.pyplot as plt
import joblib

# === 1️⃣ Veriyi Yükle ===
df = pd.read_csv(r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_combined_filtered.csv")
X = df.drop(columns=["sepsis_check"])
y = df["sepsis_check"]

# === 2️⃣ Eksik Veriyi Doldur (KNN Imputer) ===
print("🔹 Eksik veriler dolduruluyor (KNNImputer)...")
imputer = KNNImputer(n_neighbors=3)
X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

# === 3️⃣ SMOTE ile dengele ===
print("🔹 SMOTE uygulanıyor...")
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_imputed, y)

# === 4️⃣ Eğitim/Test Bölmesi ===
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# === 5️⃣ GridSearchCV ile Hyperparametre Optimizasyonu ===
print("🔹 Hyperparametre tuning başlatılıyor...")
param_grid = {
    'num_leaves': [31, 50],
    'max_depth': [-1, 10, 20],
    'learning_rate': [0.1, 0.05],
    'n_estimators': [100, 300]
}

lgbm = LGBMClassifier(random_state=42)
grid = GridSearchCV(lgbm, param_grid, cv=3, scoring='roc_auc', n_jobs=-1, verbose=1)
grid.fit(X_train, y_train)

print(f"✅ En iyi parametreler: {grid.best_params_}")

# === 6️⃣ Test Setinde Değerlendirme ===
best_model = grid.best_estimator_
y_pred = best_model.predict(X_test)
y_proba = best_model.predict_proba(X_test)[:,1]

print("\n🔹 Classification Report:")
print(classification_report(y_test, y_pred))
print("\n🔹 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print(f"\n🔹 ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")

# === ROC Curve ===
RocCurveDisplay.from_estimator(best_model, X_test, y_test)
plt.show()

# === 7️⃣ SHAP Analizi ===
print("🔹 SHAP analizi başlatılıyor...")
explainer = shap.TreeExplainer(best_model)
shap_values = explainer.shap_values(X_test)

shap.summary_plot(shap_values, X_test, plot_type="bar")

# === 8️⃣ Modeli Kaydet ===
joblib.dump(best_model, "final_lightgbm_tuned_model.pkl")
print("\n💾 Model kaydedildi: final_lightgbm_tuned_model.pkl")
