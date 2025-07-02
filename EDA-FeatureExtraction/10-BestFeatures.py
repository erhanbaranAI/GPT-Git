import pandas as pd

# Dosyayı oku
df = pd.read_csv("Sepsis-AI/output/itemid_detailed_stats_with_labels.csv")

# Eksik oranları hesapla
df = df[(df["sepsis_count"] >= 0) & (df["nonsepsis_count"] >= 0)]  # Negatif sayıları eleyelim
df["sepsis_missing_ratio"] = df["sepsis_null_count"] / (df["sepsis_count"] + df["sepsis_null_count"])
df["nonsepsis_missing_ratio"] = df["nonsepsis_null_count"] / (df["nonsepsis_count"] + df["nonsepsis_null_count"])

# Kullanılabilir itemlar (her iki grupta da eksik oranı %90'dan az)
usable_df = df[
    (df["sepsis_missing_ratio"] < 0.9) &
    (df["nonsepsis_missing_ratio"] < 0.9)
].copy()

usable_df = usable_df.reset_index(drop=True)
usable_df.insert(0, "usable_rank", usable_df.index + 1)  # sıralama ekle

print(f"\n✅ Toplam kullanılabilir item sayısı: {len(usable_df)}")
print(usable_df[["usable_rank", "itemid", "label", "sepsis_missing_ratio", "nonsepsis_missing_ratio"]].head(10))

# Belirgin farklara göre güçlü adayları filtrele
best_candidates = usable_df[
    (usable_df["mean_diff"].abs() > 5) &
    ((usable_df["sepsis_std"] - usable_df["nonsepsis_std"]).abs() > 5) &
    ((usable_df["sepsis_median"] - usable_df["nonsepsis_median"]).abs() > 5)
].copy()

best_candidates = best_candidates.reset_index(drop=True)
best_candidates.insert(0, "feature_rank", best_candidates.index + 1)

print(f"\n🏆 Ön teşhis için güçlü aday feature sayısı: {len(best_candidates)}")
print(best_candidates[[
    "feature_rank", "itemid", "label",
    "mean_diff", "sepsis_median", "nonsepsis_median",
    "sepsis_std", "nonsepsis_std",
    "sepsis_missing_ratio", "nonsepsis_missing_ratio"
]].head(91))

# Kaydet
usable_df.to_csv("Sepsis-AI/output/usable_features_full.csv", index=False)
best_candidates.to_csv("Sepsis-AI/output/best_features_ranked.csv", index=False)
print("💾 Tüm kullanılabilir ve en iyi feature'lar CSV'ye yazıldı.")
