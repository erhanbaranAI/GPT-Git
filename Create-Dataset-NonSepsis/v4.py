import pandas as pd

# === Dosya yolları ===
non_sepsis_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\non_sepsis_dataset_v2.csv"
sepsis_v5_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered_v5.csv"

# === Verileri yükle ===
non_sepsis_df = pd.read_csv(non_sepsis_path)
sepsis_v5_df = pd.read_csv(sepsis_v5_path)

# === Sütun farklarını bul ===
non_sepsis_cols = set(non_sepsis_df.columns)
sepsis_cols = set(sepsis_v5_df.columns)

only_in_non_sepsis = non_sepsis_cols - sepsis_cols
only_in_sepsis = sepsis_cols - non_sepsis_cols

print("🔍 Non-sepsis datasetine özel sütunlar:")
print(only_in_non_sepsis if only_in_non_sepsis else "Yok")

print("\n🔍 Sepsis datasetine özel sütunlar:")
print(only_in_sepsis if only_in_sepsis else "Yok")

# === sepsis_check sütunu ekle ===
non_sepsis_df['sepsis_check'] = 0
sepsis_v5_df['sepsis_check'] = 1

# (Eğer istersen buradan sonra birleştirip kaydedebiliriz!)
print("\n✅ Her iki dataset için sepsis_check sütunu eklendi.")
