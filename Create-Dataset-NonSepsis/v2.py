import pandas as pd

# === Dosya yolları ===
non_sepsis_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\non_sepsis_dataset_v2.csv"
sepsis_v5_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered_v5.csv"

# === Verileri yükle ===
non_sepsis_df = pd.read_csv(non_sepsis_path)
sepsis_v5_df = pd.read_csv(sepsis_v5_path)

# === 1️⃣ Boşluk analizi ===
missing = non_sepsis_df.isnull().mean().sort_values(ascending=False) * 100
print("🔍 Non-sepsis datasetindeki sütun bazlı boşluk oranları (%):")
print(missing)

# === 2️⃣ subject_id eşleşme kontrolü ===
non_sepsis_subjects = set(non_sepsis_df['subject_id'].unique())
sepsis_subjects = set(sepsis_v5_df['subject_id'].unique())

common_subjects = non_sepsis_subjects.intersection(sepsis_subjects)

if common_subjects:
    print(f"⚠️ Eşleşen subject_id bulundu: {len(common_subjects)} tane")
    print(list(common_subjects)[:10])  # ilk 10 tanesini örnek yazdır
else:
    print("✅ Non-sepsis ve sepsis datasetleri arasında subject_id çakışması yok.")

# === 3️⃣ (Opsiyonel) toplam boşluk oranı
row_missing = non_sepsis_df.isnull().sum().sum()
total_cells = non_sepsis_df.shape[0] * non_sepsis_df.shape[1]
overall_missing_ratio = (row_missing / total_cells) * 100
print(f"📊 Non-sepsis dataset genel boşluk oranı: {overall_missing_ratio:.2f}%")
