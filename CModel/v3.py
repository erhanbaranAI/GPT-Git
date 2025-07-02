import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, RocCurveDisplay
import matplotlib.pyplot as plt

# === Veri yükle ===
path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_combined_dataset.csv"
df = pd.read_csv(path)

# === X ve y ayır ===
X = df.drop(columns=['sepsis_check'])
y = df['sepsis_check']

# === Train / Test split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# === Model oluştur ve eğit ===
model = lgb.LGBMClassifier(random_state=42)
model.fit(X_train, y_train)

# === Tahminler ===
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# === Confusion matrix ve classification report ===
cm = confusion_matrix(y_test, y_pred)
print("🔹 Confusion Matrix:")
print(cm)

print("\n🔹 Classification Report:")
print(classification_report(y_test, y_pred, digits=4))

# === ROC-AUC ===
roc_auc = roc_auc_score(y_test, y_prob)
print(f"\n🔹 ROC-AUC: {roc_auc:.4f}")

# === ROC Eğrisi ===
RocCurveDisplay.from_estimator(model, X_test, y_test)
plt.title("ROC Curve")
plt.show()
