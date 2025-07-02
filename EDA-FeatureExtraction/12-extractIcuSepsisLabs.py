import pandas as pd

# Dosya yolları
sepsis_patients_path = "Sepsis-AI/filtered_data/icu_sepsis_patients.csv"
labevents_path = "raw/hosp/microbiologyevents.csv"
output_path = "Sepsis-AI/output/icu_sepsis_microbiologyevents.csv"

# -------------------------------
print("🔍 Sepsis hastaları dosyası yükleniyor...")
sepsis_df = pd.read_csv(sepsis_patients_path, usecols=["subject_id", "hadm_id"])

print("📦 Benzersiz hadm_id sayısı:", sepsis_df["hadm_id"].nunique())

# hadm_id'leri bir sete al
hadm_id_set = set(sepsis_df["hadm_id"].dropna().astype(int).unique())

print("🧪 Labevents dosyası parça parça okunuyor ve eşleşmeler filtreleniyor...")
chunksize = 500_000
selected_rows = []

for chunk in pd.read_csv(labevents_path, chunksize=chunksize, low_memory=False):
    if "hadm_id" not in chunk.columns:
        raise ValueError("❌ 'hadm_id' sütunu labevents.csv içinde bulunamadı.")
    matched = chunk[chunk["hadm_id"].isin(hadm_id_set)]
    if not matched.empty:
        #selected_rows.append(matched[["itemid", "hadm_id", "charttime", "value"]]) #labevents
        selected_rows.append(matched[["test_itemid", "hadm_id", "charttime", "test_name", "interpretation"]]) #microbiologyevents
# Sonuçları birleştir
if selected_rows:
    print("✅ Eşleşen veriler bulundu, kaydediliyor...")
    result_df = pd.concat(selected_rows)
    result_df.to_csv(output_path, index=False)
    print(f"💾 Çıktı başarıyla kaydedildi: {output_path}")
else:
    print("🚫 Hiçbir eşleşen laboratuvar verisi bulunamadı.")
