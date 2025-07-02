import pandas as pd

# Dosya yolu
input_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered_v3.csv"
df = pd.read_csv(input_path)
print(df.shape)
# Kullanılacak sütunlar (id'ler hariç)
data_cols = [col for col in df.columns if col not in ['subject_id', 'hadm_id', 'stay_id']]

# Her satır için boşluk sayısını hesapla
df['missing_count_row'] = df[data_cols].isnull().sum(axis=1)
df['total_cols'] = len(data_cols)

# Her subject_id için toplam boşluk ve toplam hücre sayısı
summary = df.groupby('subject_id').agg(
    total_missing = ('missing_count_row', 'sum'),
    total_cells = ('total_cols', 'count')
).reset_index()

# Her birinin oranını hesapla
summary['missing_ratio'] = (summary['total_missing'] / (summary['total_cells'] * len(data_cols))) * 100

# 100'den fazla boşluğu olanların sayısı
over_100_count = (summary['total_missing'] > 40).sum()
print(f"✅ 100'den fazla boşluğu olan subject_id sayısı: {over_100_count}")

# En çok boşluğu olan ilk 20 subject_id
top20 = summary.sort_values(by='total_missing', ascending=False).head(20)
print("\n🔹 En çok boşluğu olan ilk 20 subject_id:")
print(top20[['subject_id', 'total_missing', 'missing_ratio']])

# İstersen CSV'ye kaydet
# top20.to_csv(r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\top20_missing_subjects_detailed.csv", index=False)

# # %80 ve üstü boşluk olan subject_id'leri filtrele
# clean_df = df[~df['subject_id'].isin(summary[summary['missing_ratio'] >= 80]['subject_id'])]

# # Yeni dosya kaydet
# clean_output_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered_v3.csv"
# clean_df.to_csv(clean_output_path, index=False)

# print(f"✅ %80+ boşluk oranı olan subject_id'ler çıkarıldı. Yeni dosya: {clean_output_path}")
# print(f"Yeni satır sayısı: {clean_df.shape[0]}")
