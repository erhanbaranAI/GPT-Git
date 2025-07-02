import pandas as pd

# Dosyanın yolunu ver
path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_combined_dataset.csv"
df = pd.read_csv(path)

# subject_id, hadm_id gibi kimlik sütunlarını ayır (istersen drop edebilirsin)
id_cols = ["subject_id", "hadm_id"]
feature_cols = [col for col in df.columns if col not in id_cols]

# Tüm eksiksiz satırları seç
df_full = df[feature_cols].dropna()

# Temel bilgiler
print(f"✅ Eksiksiz satır sayısı: {df_full.shape[0]} / {df.shape[0]}")
print(f"🔹 Sepsis (1) satır sayısı: {df_full[df_full['sepsis_check'] == 1].shape[0]}")
print(f"🔹 Non-sepsis (0) satır sayısı: {df_full[df_full['sepsis_check'] == 0].shape[0]}")

# Korelasyonları hesapla
corrs = df_full.corr()["sepsis_check"].drop("sepsis_check").sort_values(key=lambda x: abs(x), ascending=False)

# En yüksek ve en düşük korelasyonları göster
print("\n🔝 En yüksek 10 korelasyon:")
print(corrs.head(10))

print("\n🔻 En düşük 10 korelasyon:")
print(corrs.tail(10))
