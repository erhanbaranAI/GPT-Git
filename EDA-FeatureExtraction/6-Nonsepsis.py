import pandas as pd
import numpy as np

# 🔹 Sepsis hastalarının stay_id listesini oku
sepsis_df = pd.read_csv("Sepsis-AI/filtered_data/icu_sepsis_patients.csv")
sepsis_stay_ids = set(sepsis_df["stay_id"].dropna().astype("Int64"))

# 🔸 Sepsis olmayan adayları toplamak için
chunksize = 10**5
nonsepsis_candidates = []

print("🔎 Sepsis olmayan adaylar taranıyor...")

for chunk in pd.read_csv("raw/icu/chartevents.csv", chunksize=chunksize, usecols=["stay_id", "itemid"]):
    chunk["stay_id"] = chunk["stay_id"].astype("Int64")
    filtered = chunk[~chunk["stay_id"].isin(sepsis_stay_ids)]
    nonsepsis_candidates.append(filtered)

nonsepsis_all = pd.concat(nonsepsis_candidates, ignore_index=True)

# 🎯 17.000 benzersiz sepsis olmayan stay_id seç
nonsepsis_unique_ids = nonsepsis_all["stay_id"].dropna().unique()
np.random.seed(42)
selected_nonsepsis_ids = set(np.random.choice(nonsepsis_unique_ids, size=17000, replace=False))

# 💾 CSV olarak istersen bu listeyi de saklayabiliriz
# pd.DataFrame({"stay_id": list(selected_nonsepsis_ids)}).to_csv("Sepsis-AI/filtered_data/nonsepsis_ids.csv", index=False)

# 🔁 Şimdi tekrar chartevents.csv içinden bu stay_id'leri çek
print("📥 Seçilen sepsis olmayan hastalara ait veriler toplanıyor...")

nonsepsis_rows_selected = []

for chunk in pd.read_csv("raw/icu/chartevents.csv", chunksize=chunksize, usecols=["stay_id", "itemid", "valuenum"]):

    chunk["stay_id"] = chunk["stay_id"].astype("Int64")
    chunk["valuenum"] = pd.to_numeric(chunk["valuenum"], errors="coerce")
    filtered = chunk[chunk["stay_id"].isin(selected_nonsepsis_ids)]
    if not filtered.empty:
        nonsepsis_rows_selected.append(filtered)

nonsepsis_df = pd.concat(nonsepsis_rows_selected, ignore_index=True)
nonsepsis_df.to_csv("Sepsis-AI/processed/chart_nonsepsis.csv", index=False)

print("✅ chart_nonsepsis.csv başarıyla oluşturuldu.")
