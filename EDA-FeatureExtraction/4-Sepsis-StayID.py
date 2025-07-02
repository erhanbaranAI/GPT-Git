# import pandas as pd

# # 1. Verileri yükle
# filtered_df = pd.read_csv("Sepsis-AI/filtered_data/filtered_patients.csv")
# icustays_df = pd.read_csv("raw/icu/icustays.csv", usecols=["subject_id", "hadm_id", "stay_id"])

# # 2. Merge işlemi: subject_id + hadm_id üzerinden eşleştir
# merged_df = pd.merge(filtered_df, icustays_df, on=["subject_id", "hadm_id"], how="left")

# # 3. Eksik stay_id olanları kontrol et (ICU’ya yatmamış olabilir)
# missing = merged_df[merged_df['stay_id'].isnull()]
# print(f"❗️ ICU kaydı olmayan hasta sayısı: {len(missing)}")

# # 4. Kaydet
# merged_df.to_csv("Sepsis-AI/filtered_data/filtered_patients_with_stay_id.csv", index=False)
# print("✅ Tamamlandı. Dosya: filtered_patients_with_stay_id.csv")



#Bu bölümde type hatasını çözdüm üst tarafta stay_id çektim################

# import pandas as pd

# df = pd.read_csv("Sepsis-AI/filtered_data/filtered_patients_with_stay_id.csv")

# # stay_id'yi tam sayı yap (boşlar varsa Int64, boşlar yoksa int)
# df['stay_id'] = df['stay_id'].astype('Int64')  # NaN içerenler için güvenli

# # Alternatif: tüm .0'ları atmak istiyorsan float → int yap:
# # df['stay_id'] = df['stay_id'].dropna().astype(int)

# df.to_csv("Sepsis-AI/filtered_data/filtered_patients_with_stay_id.csv", index=False)
# print("✅ Temizlenmiş dosya kaydedildi.")


import pandas as pd

# Orijinal CSV'yi oku
df = pd.read_csv("Sepsis-AI/filtered_data/filtered_patients_with_stay_id.csv")

# ICU'da kalmamış (stay_id boş) hastaları çıkar
df_filtered = df.dropna(subset=["stay_id"])

# stay_id sütununu int'e çevir
df_filtered["stay_id"] = df_filtered["stay_id"].astype(int)

# Yeni CSV olarak kaydet
df_filtered.to_csv("Sepsis-AI/filtered_data/icu_sepsis_patients.csv", index=False)

print("✅ ICU'da yatan sepsis hastaları filtrelenerek 'icu_sepsis_patients.csv' dosyasına kaydedildi.")
