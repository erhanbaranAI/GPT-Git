import pandas as pd

# 📥 Veriyi yükle
full_df = pd.read_csv("C:/Users/lerha/OneDrive/Masaüstü/All-in-Celsus/Sepsis-AI/Dataset/final_combined_dataset.csv")

# 📌 Gereksiz kolonları çıkar
drop_cols = ["subject_id", "hadm_id"]
data_cols = [col for col in full_df.columns if col not in drop_cols]

# 🔹 Sepsis ve non-sepsis ayır
non_sepsis_df = full_df[full_df["sepsis_check"] == 0].copy()
sepsis_df = full_df[full_df["sepsis_check"] == 1].copy()

# 🔹 Non-sepsis eksiklik sayısına göre sırala
non_sepsis_df["missing_count"] = non_sepsis_df[data_cols].isnull().sum(axis=1)
non_sepsis_df = non_sepsis_df.sort_values("missing_count")

# 🔹 2889 non-sepsis ve 2889 sepsis al
balanced_non_sepsis = non_sepsis_df.head(2889)
balanced_sepsis = sepsis_df.sample(2889, random_state=42)

# 🔹 Birleştir ve korelasyon hesapla
balanced_df = pd.concat([balanced_sepsis, balanced_non_sepsis], ignore_index=True)
corr = balanced_df.corr()["sepsis_check"].drop("sepsis_check")

# 🔹 0.01 ile -0.01 aralığında kalan zayıf feature'ları bul
weak_features = corr[(corr > -0.1) & (corr < 0.1)].index.tolist()
print(f"✅ {len(weak_features)} özellik 0.1 ile -0.1 aralığında korelasyona sahip ve çıkarılacak.")
print("📝 Çıkarılacak ilk 5 özellik örneği:", weak_features[:5])

# 🔹 Bu feature'ları tam dataset'ten çıkar
final_df = full_df.drop(columns=weak_features)

# 💾 Yeni CSV'yi kaydet
output_path = "C:/Users/lerha/OneDrive/Masaüstü/All-in-Celsus/Sepsis-AI/Dataset/final_combined_filtered.csv"
final_df.to_csv(output_path, index=False)

# 📊 Shape bilgisi
print(f"✅ Yeni dosya kaydedildi: {output_path}")
print(f"📊 Yeni dataset boyutu: {final_df.shape}")
