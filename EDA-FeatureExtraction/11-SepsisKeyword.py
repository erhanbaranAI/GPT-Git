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

target_csv_paths = [
    #"raw/icu/d_items.csv",
    #"raw/hosp/d_labitems.csv",
    "raw/hosp/microbiologyevents.csv",
    "raw/icu/inputevents.csv",
    "raw/icu/outputevents.csv",
]

output_file = "sepsis_keyword_matchesv2.txt"
chunksize = 1_000_000

with open(output_file, "w", encoding="utf-8") as out:
    for csv_path in target_csv_paths:
        print(f"🔍 Şu an işleniyor: {csv_path} ...")
        
        if not os.path.exists(csv_path):
            out.write(f"\n❌ Dosya bulunamadı: {csv_path}\n")
            continue

        try:
            # Başlıkları al ve yaz
            header = pd.read_csv(csv_path, nrows=0)
            header_line = ",".join(header.columns.astype(str))

            out.write(f"\n📂 CSV dosyası: {os.path.basename(csv_path)}\n")
            out.write(f"📑 Sütunlar: {header_line}\n")

            matched_any = False

            for chunk in pd.read_csv(csv_path, chunksize=chunksize, low_memory=False):
                for kw in keywords:
                    matches = chunk[chunk.astype(str).apply(lambda row: row.str.contains(kw, case=False, na=False)).any(axis=1)]

                    if not matches.empty:
                        matched_any = True
                        out.write(f"\n🔎 Anahtar Kelime: {kw}\n")
                        for _, row in matches.iterrows():
                            out.write(",".join(map(str, row.values)) + "\n")

            if not matched_any:
                out.write(f"\n🚫 {csv_path} içinde eşleşme bulunamadı.\n")

        except Exception as e:
            out.write(f"\n⚠️ HATA - {csv_path} | {str(e)}\n")
