import pandas as pd

# 📥 Dosya yolu
path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_combined_dataset.csv"
df = pd.read_csv(path)

print(f"✅ Dataset shape: {df.shape}")

# === Sütun bazında eksik oranları ===
missing_col = df.isnull().mean().sort_values(ascending=False) * 100
print("\n🔹 Sütun bazında eksik oranları (en yüksekten düşüğe):")
print(missing_col.to_string())

# === Satır bazında eksik oranları ===
df['missing_row_percent'] = df.isnull().mean(axis=1) * 100

# Satır aralık analizi
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
row_bin_counts = pd.cut(df['missing_row_percent'], bins).value_counts().sort_index()

print("\n🔹 Satır bazında eksik oran dağılımı (%):")
for interval, count in row_bin_counts.items():
    print(f"{interval}: {count} satır")

# === Özet ===
print("\n🔹 Genel eksik veri oranı özet:")
print(f"Ortalama sütun bazında eksik oranı: {missing_col.mean():.2f}%")
print(f"Ortalama satır bazında eksik oranı: {df['missing_row_percent'].mean():.2f}%")
print(f"Tam dolu satır sayısı: {(df['missing_row_percent'] == 0).sum()}")
print(f"%50'den fazla eksik olan satır sayısı: {(df['missing_row_percent'] > 50).sum()}")

# (Opsiyonel: dosyaya yazmak istersen)
# missing_col.to_csv("missing_column_analysis.csv")
# df[['missing_row_percent']].to_csv("missing_row_analysis.csv")

