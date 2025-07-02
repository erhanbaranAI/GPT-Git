import pandas as pd

# Dosya yolları
stats_csv = "Sepsis-AI/output/itemid_detailed_stats.csv"
d_items_csv = "raw/icu/d_items.csv"
output_csv = "Sepsis-AI/output/itemid_detailed_stats_with_labels.csv"

# 1. İstatistik verisini oku
stats_df = pd.read_csv(stats_csv)

# 2. d_items.csv dosyasını oku
d_items_df = pd.read_csv(d_items_csv, usecols=["itemid", "label"])

# 3. Merge işlemi (itemid'ye göre)
merged_df = stats_df.merge(d_items_df, on="itemid", how="left")

# 4. Eşleşmeyen itemid’leri print et
missing_items = merged_df[merged_df["label"].isna()]["itemid"].tolist()
if missing_items:
    print("❗ Eşleşmeyen itemid'ler (d_items.csv'de bulunamadı):")
    for item in missing_items:
        print(f"  - {item}")

# 5. Sonuçları yeni CSV’ye yaz
merged_df.to_csv(output_csv, index=False)
print(f"✅ Etiketli detaylı istatistikler CSV olarak kaydedildi: {output_csv}")
