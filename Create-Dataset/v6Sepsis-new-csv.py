import pandas as pd
import os

# 📁 Klasör ayarları
DATA_DIR = "raw/hosp/"
ICU_DIR = "raw/icu/"
OUTPUT_DIR = "Sepsis-AI/filtered_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1️⃣ Sepsis ICD kodlarını al
icd_desc_path = os.path.join(DATA_DIR, "d_icd_diagnoses.csv")
icd_df = pd.read_csv(icd_desc_path)

sepsis_icd_codes = icd_df[icd_df['long_title'].str.contains("sepsis", case=False, na=False)]['icd_code'].unique()
print(f"🎯 Sepsis ile ilişkili {len(sepsis_icd_codes)} ICD kodu bulundu.")

# 2️⃣ Sepsis teşhisi konmuş hospital admission'ları bul
diag_path = os.path.join(DATA_DIR, "diagnoses_icd.csv")
diag_df = pd.read_csv(diag_path)

sepsis_patients = diag_df[diag_df['icd_code'].isin(sepsis_icd_codes)][['subject_id', 'hadm_id']]
sepsis_patients = sepsis_patients.drop_duplicates()

# 3️⃣ İlk hospital admission'ı al
first_hadm = sepsis_patients.groupby("subject_id")["hadm_id"].min().reset_index()

# 4️⃣ ICU stay_id'lerini al ve ilkini seç
icustays_path = os.path.join(ICU_DIR, "icustays.csv")
icu_df = pd.read_csv(icustays_path)

# Sepsisli hospital admission'lardan olan ICU kalışları
sepsis_icu = pd.merge(icu_df, first_hadm, on="subject_id")
sepsis_icu = sepsis_icu[sepsis_icu["hadm_id_y"] == sepsis_icu["hadm_id_x"]]

# İlk ICU stay'i seç
first_icu = sepsis_icu.groupby("subject_id")["stay_id"].min().reset_index()

# 5️⃣ Birleştir ve kaydet
result = pd.merge(first_hadm, first_icu, on="subject_id")
output_path = os.path.join(OUTPUT_DIR, "icu_sepsis_filtered.csv")
result.to_csv(output_path, index=False)

print(f"✅ İlk sepsis hospital admission ve ICU stay seçildi, kaydedildi: {output_path}")
print(result.head())
