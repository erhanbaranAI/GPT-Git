import os
import pandas as pd

keywords = [
    "WBC", "White Blood Cell", "Leukocyte", "Lactate", "Glucose", "Creatinine", "Cr",
    "Bilirubin", "Platelet", "Plt", "BUN", "HCO3", "Base Excess", "pH",
    "O2 Saturation", "Oxygen Saturation", "SpO2", "SaO2", "FiO2",
    "pO2", "pCO2", "PaO2", "PaCO2",
    "Heart Rate", "HR", "Pulse",
    "Respiratory Rate", "RR", "Temperature", "Temp",
    "MAP", "Mean Arterial Pressure",
    "Urine Output", "Urine", "Urinary Output", "UO", "Catheter",
    "Procalcitonin", "CRP", "C-Reactive Protein",
    "Blood Culture", "Culture", "Infection"
]

# 📁 Dosya yolları
sepsis_path = "Sepsis-AI/filtered_data/icu_sepsis_patients.csv"
targets = [
    ("raw/hosp/microbiologyevents.csv", "hadm_id", "Sepsis-AI/output/icu_sepsis_microbio.csv", "Sepsis-AI/output/microbio_itemid_usage_counts.txt"),
    ("raw/icu/inputevents.csv", "stay_id", "Sepsis-AI/output/icu_sepsis_inputevents.csv", "Sepsis-AI/output/inputevents_itemid_usage_counts.txt"),
    ("raw/icu/outputevents.csv", "stay_id", "Sepsis-AI/output/icu_sepsis_outputevents.csv", "Sepsis-AI/output/outputevents_itemid_usage_counts.txt"),
]

# 🧠 Sepsis hastaları yükleniyor
print("🔍 Sepsis hastaları dosyası yükleniyor...")
sepsis_df = pd.read_csv(sepsis_path, usecols=["stay_id", "hadm_id"])
stay_id_set = set(sepsis_df["stay_id"].dropna().astype(int))
hadm_id_set = set(sepsis_df["hadm_id"].dropna().astype(int))

chunksize = 500_000

for path, key, output_csv, output_txt in targets:
    print(f"\n📄 İşleniyor: {path}")
    if not os.path.exists(path):
        print(f"❌ Dosya bulunamadı: {path}")
        continue

    id_set = stay_id_set if key == "stay_id" else hadm_id_set
    selected_rows = []

    for chunk in pd.read_csv(path, chunksize=chunksize, low_memory=False):
        if key not in chunk.columns:
            print(f"⚠️ {key} sütunu {path} dosyasında bulunamadı.")
            continue
        matched = chunk[chunk[key].isin(id_set)]
        if not matched.empty:
            keep_cols = [col for col in ["itemid", key, "charttime", "value"] if col in matched.columns]
            selected_rows.append(matched[keep_cols])

    if selected_rows:
        result_df = pd.concat(selected_rows)
        result_df.to_csv(output_csv, index=False)
        print(f"✅ Filtrelenmiş veriler kaydedildi: {output_csv}")

        # itemid sayımı
        if "itemid" in result_df.columns:
            item_counts = result_df["itemid"].value_counts().reset_index()
            item_counts.columns = ["itemid", "count"]
            with open(output_txt, "w", encoding="utf-8") as f:
                for _, row in item_counts.iterrows():
                    f.write(f"{int(row['itemid'])}: {int(row['count'])}\n")
            print(f"📊 itemid kullanım sayıları yazıldı: {output_txt}")
        else:
            print(f"⚠️ itemid sütunu {output_csv} dosyasında bulunamadı.")
    else:
        print("🚫 Eşleşen veri bulunamadı.")
