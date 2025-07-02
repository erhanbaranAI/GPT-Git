import pandas as pd

# === Dosya yolları ===
input_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\non_sepsis_dataset.csv"
output_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\non_sepsis_dataset_v2.csv"

# === Veri yükle ===
df = pd.read_csv(input_path)

# === Başlangıç boşluk sayısı ===
initial_missing = df.isnull().sum().sum()
print(f"🔹 V4 toplam boşluk sayısı: {initial_missing}")

# === Drop edilecek sütunlar ===
drop_cols = [
    "ID220227_std", "ID220227_first", "ID220227_mean", "ID220227_min",
    "ID220227_max", "ID220227_diff", "ID220227_last",
    "ID50817_std", "BaseExcess_std", "ID220235_std",
    "ID220224_std", "ID223830_std", "ID224689_std"
]

# === Sütunları drop yap ===
df_v5 = df.drop(columns=drop_cols, errors='ignore')

# === Yeni boşluk sayısı ===
new_missing = df_v5.isnull().sum().sum()
print(f"✅ V5 toplam boşluk sayısı (drop sonrası): {new_missing}")

# === Yeni dosyayı kaydet ===
df_v5.to_csv(output_path, index=False)
print(f"💾 Yeni dosya kaydedildi: {output_path}")
