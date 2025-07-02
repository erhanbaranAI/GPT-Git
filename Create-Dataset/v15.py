import pandas as pd
import numpy as np

# 📥 Dataseti yükle (yolu kendine göre ayarla)
df = pd.read_csv("C:/Users/lerha/OneDrive/Masaüstü/All-in-Celsus/Sepsis-AI/Dataset/final_combined_dataset.csv")

# 🔹 Sadece sayısal sütunlar ve sepsis_check ile korelasyon hesapla
num_df = df.select_dtypes(include=[np.number])

# Sepsis_check ile korelasyon
correlations = num_df.corr()['sepsis_check'].drop('sepsis_check').sort_values(key=np.abs, ascending=False)

# 🔍 Sonuçları yazdır
print("\n🔹 Değişkenlerin sepsis_check ile korelasyonu (mutlak değere göre büyükten küçüğe):")
print(correlations)

# En yüksek ve en düşük 10'u ayrı göstermek istersen:
print("\n🔹 En yüksek 10 korelasyon:")
print(correlations.head(10))

print("\n🔹 En düşük 10 korelasyon:")
print(correlations.tail(10))
