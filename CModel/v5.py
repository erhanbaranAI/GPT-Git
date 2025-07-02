import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier

# 📥 Dataset'i yükle
df = pd.read_csv("C:/Users/lerha/OneDrive/Masaüstü/All-in-Celsus/Sepsis-AI/Dataset/final_combined_filtered.csv")

# ✅ Sepsis_check var mı kontrol et
if "sepsis_check" not in df.columns:
    raise ValueError("❌ 'sepsis_check' kolonu dataset içinde bulunamadı!")

# 🎯 Y hedefi ve X özellikler
y = df["sepsis_check"]
X = df.drop(columns=["sepsis_check"])

# ✂️ Eğitim / test ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 🚀 Modeller
models = {
    "LightGBM": LGBMClassifier(verbose=-1, random_state=42),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42),
    "CatBoost": CatBoostClassifier(verbose=0, random_state=42)
}

# 🔍 Eğit ve değerlendir
for name, model in models.items():
    print(f"\n⚡ {name} Modeli Eğitiliyor...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print(f"\n🔹 {name} Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print(f"\n🔹 {name} Classification Report:")
    print(classification_report(y_test, y_pred))

    roc_auc = roc_auc_score(y_test, y_proba)
    print(f"🔹 {name} ROC-AUC: {roc_auc:.4f}")
