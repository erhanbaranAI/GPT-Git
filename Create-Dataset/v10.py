import pandas as pd
import numpy as np

# === Dosya yolları ===
input_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered.csv"
output_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered_v2.csv"

# === Veri yükle ===
df = pd.read_csv(input_path)

# === subject_id + hadm_id bazında duplicate birleştirme ===
merge_cols = [col for col in df.columns if col not in ["stay_id", "subject_id", "hadm_id"]]

merged = df.groupby(['subject_id', 'hadm_id'])[merge_cols].agg(
    lambda x: x.dropna().iloc[0] if not x.dropna().empty else np.nan
).reset_index()

# === Kaydet ===
merged.to_csv(output_path, index=False)
print(f"✅ Yeni dataset kaydedildi: {output_path}")
print(f"Toplam satır sayısı: {merged.shape[0]}")

# === Boş oran analizi ===
data_cols = [col for col in merged.columns if col not in ['subject_id', 'hadm_id']]
merged['missing_percent'] = merged[data_cols].isnull().mean(axis=1) * 100

for threshold in range(100, -10, -10):
    count = (merged['missing_percent'] > threshold).sum()
    print(f">%{threshold} boşluğa sahip satır sayısı: {count}")
