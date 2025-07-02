import pandas as pd

# Dosya yolu
path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered_v3.csv"
df = pd.read_csv(path)

# Sütunları belirle
data_cols = [col for col in df.columns if col not in ['subject_id', 'hadm_id', 'stay_id']]

# Her satır için boşluk sayısı
df["missing_count"] = df[data_cols].isnull().sum(axis=1)

# 70+ boşluk olanları çıkar
clean_df = df[df["missing_count"] < 70].drop(columns="missing_count")

# Yeni dosyayı kaydet
output_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered_v4.csv"
clean_df.to_csv(output_path, index=False)

print(f"✅ 70+ boşluğu olan satırlar çıkarıldı. Yeni dosya: {output_path}")
print(f"Yeni satır sayısı: {clean_df.shape[0]}")

# Sütun bazlı boşluk oranı
missing_col_ratio = clean_df[data_cols].isnull().mean().sort_values(ascending=False) * 100

# En çok eksik olanları yazdır
print("\n🔹 Sütun bazlı eksik oranları (en çok eksikten en aza):")
print(missing_col_ratio)

# İstersen bunu bir txt'ye de kaydedebilirsin:
missing_col_ratio.to_csv(r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\missing_columns_analysisv2.csv")
print("🔍 Sütun boşluk oranları CSV'ye kaydedildi.")
