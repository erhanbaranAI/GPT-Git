import pandas as pd

# Dosya yolları
sepsis_patients_path = "Sepsis-AI/filtered_data/icu_sepsis_patients.csv"
chartevents_path = "raw/icu/inputevents.csv"
output_path = "Sepsis-AI/output/icu_sepsis_inputevents.csv"
itemid_count_output = "Sepsis-AI/output/inputevents_itemid_usage_counts.txt"

# 🔍 Sepsis hastaları yükleniyor
print("🔍 Sepsis hastaları dosyası yükleniyor...")
sepsis_df = pd.read_csv(sepsis_patients_path, usecols=["stay_id"])
stay_id_set = set(sepsis_df["stay_id"].dropna().astype(int).unique())
print("📦 Benzersiz stay_id sayısı:", len(stay_id_set))

# 🧪 Chartevents dosyası parça parça okunuyor ve filtreleniyor
chunksize = 500_000
selected_rows = []

for chunk in pd.read_csv(chartevents_path, chunksize=chunksize, low_memory=False):
    if "stay_id" not in chunk.columns:
        raise ValueError("❌ 'stay_id' sütunu chartevents.csv içinde bulunamadı.")
    
    matched = chunk[chunk["stay_id"].isin(stay_id_set)]
    if not matched.empty:
        selected_rows.append(matched[["itemid", "stay_id", "starttime", "amount"]])


# Sonuçları birleştir
if selected_rows:
    print("✅ Eşleşen veriler bulundu, kaydediliyor...")
    result_df = pd.concat(selected_rows)
    result_df.to_csv(output_path, index=False)
    print(f"💾 Çıktı kaydedildi: {output_path}")

    # 🔢 itemid kullanımlarını say
    item_counts = result_df["itemid"].value_counts().reset_index()
    item_counts.columns = ["itemid", "count"]

    # 📄 TXT dosyasına yaz
    with open(itemid_count_output, "w", encoding="utf-8") as f:
        for _, row in item_counts.iterrows():
            f.write(f"{int(row['itemid'])}: {int(row['count'])}\n")

    print(f"📊 itemid kullanım istatistikleri kaydedildi: {itemid_count_output}")
else:
    print("🚫 Hiçbir eşleşen chartevents verisi bulunamadı.")
