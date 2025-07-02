import pandas as pd
import numpy as np

# 📌 Sepsis hastalarının stay_id listesini oku
sepsis_df = pd.read_csv("Sepsis-AI/filtered_data/icu_sepsis_patients.csv")
sepsis_stay_ids = set(sepsis_df["stay_id"].dropna().astype(int))

# 🔄 Aşama 1: chartevents.csv dosyasından sadece sepsis hastalarına ait verileri al
chunksize = 10**5
sepsis_chart_rows = []
nonsepsis_candidates = []

print("🔎 Sepsis ve aday olmayan hasta verileri okunuyor...")

for chunk in pd.read_csv("raw/icu/chartevents.csv", chunksize=chunksize, usecols=["stay_id", "itemid", "valuenum"]):
    chunk["stay_id"] = chunk["stay_id"].astype("Int64")  # Nullable int
    chunk["valuenum"] = pd.to_numeric(chunk["valuenum"], errors="coerce")
    sepsis_rows = chunk[chunk["stay_id"].isin(sepsis_stay_ids)]
    if not sepsis_rows.empty:
        sepsis_chart_rows.append(sepsis_rows)

    nonsepsis_rows = chunk[~chunk["stay_id"].isin(sepsis_stay_ids)]
    nonsepsis_candidates.append(nonsepsis_rows[["stay_id", "itemid"]])

print("✅ Sepsis verileri toplandı. Şimdi yazılıyor...")

# 🔄 Sepsis grubunun verisini birleştir ve kaydet
sepsis_chart_df = pd.concat(sepsis_chart_rows, ignore_index=True)
sepsis_chart_df.to_csv("Sepsis-AI/processed/chart_sepsis.csv", index=False)
