import pandas as pd

# 📥 Veriyi yükle
df = pd.read_csv("C:/Users/lerha/OneDrive/Masaüstü/All-in-Celsus/Sepsis-AI/Dataset/final_combined_dataset.csv")

# 📌 Gereksiz kolonları çıkar
drop_cols = ["subject_id", "hadm_id"]
data_cols = [col for col in df.columns if col not in drop_cols]

# Non-sepsis ve sepsis ayrı
non_sepsis_df = df[df["sepsis_check"] == 0].copy()
sepsis_df = df[df["sepsis_check"] == 1].copy()

# Non-sepsis için eksiklik oranını hesapla
non_sepsis_df["missing_count"] = non_sepsis_df[data_cols].isnull().sum(axis=1)
non_sepsis_df = non_sepsis_df.sort_values("missing_count")

# 2889 non-sepsis seç
balanced_non_sepsis = non_sepsis_df.head(2889)

# Sepsis zaten 2889
balanced_sepsis = sepsis_df.sample(2889, random_state=42)

# Birleştir
balanced_df = pd.concat([balanced_sepsis, balanced_non_sepsis], ignore_index=True)

# Korelasyon hesapla
corr = balanced_df.corr()["sepsis_check"].drop("sepsis_check").sort_values(key=lambda x: abs(x), ascending=False)

# Sonuçları yazdır
print("\n🔹 En yüksek 10 korelasyon:")
print(corr.head(10))
print("\n🔹 En düşük 10 korelasyon:")
print(corr.tail(10))
