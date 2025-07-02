# import pandas as pd
# import matplotlib.pyplot as plt

# # === Dosyanın yolu ===
# path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset.csv"
# df = pd.read_csv(path)

# # === subject_id başına hadm_id ve stay_id çeşitliliği ===
# summary = df.groupby("subject_id").agg(
#     hadm_id_count=("hadm_id", "nunique"),
#     stay_id_count=("stay_id", "nunique")
# ).reset_index()

# # === İlk 10 örnek göster ===
# print("🔹 İlk 10 subject_id için farklı hadm_id ve stay_id sayısı:")
# print(summary.head(10))

# # === Histogram: kaç hastada kaç stay var? ===
# plt.figure(figsize=(8,5))
# summary["stay_id_count"].value_counts().sort_index().plot(kind="bar")
# plt.xlabel("Farklı ICU Stay Sayısı (stay_id)")
# plt.ylabel("Hasta Sayısı")
# plt.title("Her subject_id için farklı ICU stay sayısı dağılımı")
# plt.tight_layout()
# plt.show()

# # === Histogram: kaç hastada kaç admission var? ===
# plt.figure(figsize=(8,5))
# summary["hadm_id_count"].value_counts().sort_index().plot(kind="bar", color="orange")
# plt.xlabel("Farklı Hospital Admission Sayısı (hadm_id)")
# plt.ylabel("Hasta Sayısı")
# plt.title("Her subject_id için farklı hospital admission sayısı dağılımı")
# plt.tight_layout()
# plt.show()

# # === Tüm summary'yi kaydet (isteğe bağlı) ===
# summary.to_csv(r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\subject_summary.csv", index=False)
# print("✅ Özet CSV dosyası kaydedildi: subject_summary.csv")


import pandas as pd

# Veri setini yükle
path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered.csv"
df = pd.read_csv(path)

# ICU stay sayısı
stay_counts = df.groupby("subject_id")["stay_id"].nunique().sort_values(ascending=False)
print("🔹 En fazla farklı ICU stay_id'ye sahip ilk 20 subject_id:")
print(stay_counts.head(30))

# Hospital admission sayısı
hadm_counts = df.groupby("subject_id")["hadm_id"].nunique().sort_values(ascending=False)
print("\n🔹 En fazla farklı hospital admission (hadm_id)'e sahip ilk 20 subject_id:")
print(hadm_counts.head(30))
