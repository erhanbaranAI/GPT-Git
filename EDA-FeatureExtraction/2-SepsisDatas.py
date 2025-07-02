import os
import pandas as pd

#Sepsis hastalarının diğer klasörlerdeki veri eşleşmesi

# Sepsis hasta bilgilerini oku
filtered = pd.read_csv("Sepsis-AI/filtered_data/filtered_patients.csv")
subject_ids = set(filtered['subject_id'])
hadm_ids = set(filtered['hadm_id'])

# ICU stay_id kontrolü için varsa kullan
stay_ids = set()
if 'stay_id' in filtered.columns:
    stay_ids = set(filtered['stay_id'])

# İşlenecek klasörler
base_dirs = ['raw/hosp', 'raw/icu']
chunk_size = 100_000
results = []

for base_dir in base_dirs:
    for file in os.listdir(base_dir):
        if file.endswith(".csv"):
            path = os.path.join(base_dir, file)
            subject_total = 0
            hadm_total = 0
            stay_total = 0
            try:
                for chunk in pd.read_csv(path, chunksize=chunk_size, low_memory=False):
                    cols = chunk.columns
                    if 'subject_id' in cols:
                        subject_total += chunk['subject_id'].isin(subject_ids).sum()
                    if 'hadm_id' in cols:
                        hadm_total += chunk['hadm_id'].isin(hadm_ids).sum()
                    if 'stay_id' in cols:
                        stay_total += chunk['stay_id'].isin(stay_ids).sum()
                results.append({
                    "dosya": file,
                    "klasör": base_dir,
                    "subject_id eşleşme": subject_total,
                    "hadm_id eşleşme": hadm_total,
                    "stay_id eşleşme": stay_total,
                    "toplam eşleşme": subject_total + hadm_total + stay_total
                })
            except Exception as e:
                results.append({
                    "dosya": file,
                    "klasör": base_dir,
                    "subject_id eşleşme": "Hata",
                    "hadm_id eşleşme": "Hata",
                    "stay_id eşleşme": "Hata",
                    "toplam eşleşme": f"Hata: {e}"
                })

# Sonuçları kaydet
df_results = pd.DataFrame(results)
df_results.sort_values("toplam eşleşme", ascending=False, inplace=True)
df_results.to_excel("Sepsis-AI/filtered_data/sepsis_data_density.xlsx", index=False)

print("✅ Tamamlandı! Sonuçlar: sepsis_data_density.xlsx")
