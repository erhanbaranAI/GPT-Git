import pandas as pd

# 📁 Dosya yolu
path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset.csv"
df = pd.read_csv(path)

# 1️⃣ subject_id + hadm_id tekrar edenleri bul
dupes = df.groupby(['subject_id', 'hadm_id']).size().reset_index(name='count')
dupes = dupes[dupes['count'] > 1]

# 2️⃣ Satır bazında boşluk (eksik) sayısı hesapla
missing_per_row = df.isnull().sum(axis=1)
df_missing_summary = pd.DataFrame({
    'subject_id': df['subject_id'],
    'hadm_id': df['hadm_id'],
    'stay_id': df['stay_id'],
    'missing_count': missing_per_row
}).sort_values(by='missing_count', ascending=False)

# 3️⃣ Dosyaya yaz
output_txt = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\missing_report2.txt"
with open(output_txt, 'w', encoding='utf-8') as f:
    f.write("=== DUPLICATE subject_id + hadm_id ===\n")
    for _, row in dupes.iterrows():
        f.write(f"subject_id: {row['subject_id']} hadm_id: {row['hadm_id']} count: {row['count']}\n")
    
    f.write("\n=== EN FAZLA BOŞLUĞU OLANLAR ===\n")
    for _, row in df_missing_summary.iterrows():
        f.write(f"subject_id: {row['subject_id']}, hadm_id: {row['hadm_id']}, stay_id: {row['stay_id']}, boşluk: {row['missing_count']}\n")

print(f"✅ Rapor yazıldı: {output_txt}")
