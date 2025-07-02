import pandas as pd
import os

# 📁 Klasör ayarları
DATA_DIR = "raw/hosp/"
OUTPUT_DIR = "Sepsis-AI/filtered_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Sepsis ICD kodlarını al
icd_desc_path = os.path.join(DATA_DIR, "d_icd_diagnoses.csv")
icd_df = pd.read_csv(icd_desc_path)

# 'sepsis' içeren ICD kodlarını filtrele (büyük/küçük harf duyarsız)
sepsis_icd_codes = icd_df[icd_df['long_title'].str.contains("sepsis", case=False, na=False)]['icd_code'].unique()
print(f"🎯 Sepsis ile ilişkili {len(sepsis_icd_codes)} ICD kodu bulundu.")

# 2. diagnoses_icd.csv içinden sepsis kodlu hastaları bul   
diag_path = os.path.join(DATA_DIR, "diagnoses_icd.csv")
diag_df = pd.read_csv(diag_path)

# Sadece sepsis ICD kodlarına sahip satırları al
sepsis_patients = diag_df[diag_df['icd_code'].isin(sepsis_icd_codes)][['subject_id', 'hadm_id']].drop_duplicates()

print(f"🧠 Sepsis tanısı almış toplam {len(sepsis_patients)} benzersiz hasta kaydı bulundu.")

# 3. CSV olarak kaydet
output_path = os.path.join(OUTPUT_DIR, "filtered_patients.csv")
sepsis_patients.to_csv(output_path, index=False)
print(f"✅ Filtrelenmiş hasta listesi kaydedildi: {output_path}")
