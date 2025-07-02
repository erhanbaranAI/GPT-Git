import pandas as pd
import numpy as np

# === Dosya yolları ===
v5_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered_v5.csv"
v6_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered_v6.csv"
v6_test_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered_v6_test.csv"

# === V5 YÜKLE ===
df = pd.read_csv(v5_path)

# === Boşluk oranını hesapla ===
data_cols = [col for col in df.columns if col not in ['subject_id', 'hadm_id', 'stay_id']]
df['missing_ratio'] = df[data_cols].isnull().mean(axis=1)

# === V6: %10'dan az boşluğu olanlar ===
v6 = df[df['missing_ratio'] < 0.10].drop(columns=['missing_ratio'])
v6.to_csv(v6_path, index=False)

# === V6_test: diğerleri ===
v6_test = df[df['missing_ratio'] >= 0.10].drop(columns=['missing_ratio'])
v6_test.to_csv(v6_test_path, index=False)

# === Özet Bilgi ===
print(f"✅ V6 oluşturuldu: {v6.shape[0]} satır")
print(f"✅ V6_test oluşturuldu: {v6_test.shape[0]} satır")
print(f"📝 V6 toplam boşluk oranı: {v6[data_cols].isnull().mean().mean() * 100:.2f}%")
print(f"📝 V6_test toplam boşluk oranı: {v6_test[data_cols].isnull().mean().mean() * 100:.2f}%")
