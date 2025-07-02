import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import cross_val_score

# === Dosya yolları ===
v6_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered_v6.csv"
v6_test_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered_v6_test.csv"

# === Veri yükle ===
v6 = pd.read_csv(v6_path)
v6_test = pd.read_csv(v6_test_path)

# === Hangi sütunu dolduracağımızı seçelim ===
target_col = "Creatinine_mean"  # İstediğin başka bir sütunu seçebilirsin

# === Eğitim için hedefi boş olmayanları ayır ===
train_df = v6[v6[target_col].notnull()]
test_df = v6_test[v6_test[target_col].isnull()]

# === Drop edilecek sütunları belirle ===
drop_cols = ["subject_id", "hadm_id", "stay_id", target_col]
drop_cols = [col for col in drop_cols if col in train_df.columns]

X_train = train_df.drop(columns=drop_cols)
y_train = train_df[target_col]

X_test = test_df.drop(columns=drop_cols)

# === XGBoost model ===
model = XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)

from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
import numpy as np

kf = KFold(n_splits=5, shuffle=True, random_state=42)
rmses = []

for train_idx, val_idx in kf.split(X_train):
    X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
    y_tr, y_val = y_train.iloc[train_idx], y_train.iloc[val_idx]
    
    model.fit(X_tr.fillna(-999), y_tr)
    preds = model.predict(X_val.fillna(-999))
    rmse = np.sqrt(mean_squared_error(y_val, preds))
    rmses.append(rmse)

print(f"✅ CV RMSE: {np.mean(rmses):.4f} (+/- {np.std(rmses):.4f})")


# === Modeli eğit ===
model.fit(X_train.fillna(-999), y_train)

# === Eksikleri tahmin et ===
preds = model.predict(X_test.fillna(-999))
v6_test.loc[v6_test[target_col].isnull(), target_col] = preds

# === Tahmin sonrası dosyayı kaydet ===
output_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filled.csv"
combined = pd.concat([v6, v6_test], ignore_index=True)
combined.to_csv(output_path, index=False)
print(f"💾 Tahminler uygulandı ve yeni dosya kaydedildi: {output_path}")
