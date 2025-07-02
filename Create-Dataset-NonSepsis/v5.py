import pandas as pd

# === Dosya yolları ===
non_sepsis_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\non_sepsis_dataset_v2.csv"
sepsis_v5_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered_v5.csv"
output_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_combined_dataset.csv"

# === Verileri yükle ===
non_sepsis_df = pd.read_csv(non_sepsis_path)
sepsis_v5_df = pd.read_csv(sepsis_v5_path)

# === Non-sepsis datasetinden özel sütunları drop et ===
non_sepsis_df = non_sepsis_df.drop(columns=['stay_id', 'missing_ratio'], errors='ignore')

# === Her iki datasetten ortak istenmeyen sütunları drop et ===
drop_cols = ['subject_id', 'hadm_id', 'missing_count_row', 'total_cols']
non_sepsis_df = non_sepsis_df.drop(columns=drop_cols, errors='ignore')
sepsis_v5_df = sepsis_v5_df.drop(columns=drop_cols, errors='ignore')

# === sepsis_check ekle ===
non_sepsis_df['sepsis_check'] = 0
sepsis_v5_df['sepsis_check'] = 1

# === Birleştir ===
combined_df = pd.concat([non_sepsis_df, sepsis_v5_df], ignore_index=True)

# === CSV olarak kaydet ===
combined_df.to_csv(output_path, index=False)

print(f"✅ Tüm veri seti birleştirildi ve kaydedildi: {output_path}")
print(f"📊 Final dataset shape: {combined_df.shape}")
