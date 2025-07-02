import pandas as pd

# === Dosya yükle ===
path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered.csv"
df = pd.read_csv(path)

# === Duplicate olan subject_id + hadm_id gruplarını bul ===
dups = df.groupby(['subject_id', 'hadm_id']).filter(lambda x: len(x) > 1)

# === Sonuçları tutacağımız liste ===
results = []

# === Gruplar için kontrol yap ===
for (subj, hadm), group in dups.groupby(['subject_id', 'hadm_id']):
    rows = group.drop(columns=['subject_id', 'hadm_id', 'stay_id'])
    
    if len(rows) < 2:
        continue  # sadece ikili karşılaştırmaya odaklanıyoruz
    
    # İlk iki satırı karşılaştıralım (genelde ikili duplicate var)
    row1 = rows.iloc[0].notnull()
    row2 = rows.iloc[1].notnull()
    
    both_filled = (row1 & row2).sum()
    diff_filled = ((row1 ^ row2)).sum()
    both_empty = (~row1 & ~row2).sum()
    
    results.append({
        'subject_id': subj,
        'hadm_id': hadm,
        'both_filled': both_filled,
        'diff_filled': diff_filled,
        'both_empty': both_empty
    })

# === DataFrame'e çevir ve incele ===
result_df = pd.DataFrame(results)
print(result_df.sort_values(by='diff_filled', ascending=False).head(10))

# İsteyen olursa CSV'ye de yazdırabilirsin
output_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\duplicate_fill_analysis.csv"
result_df.to_csv(output_path, index=False)
print(f"✅ Analiz CSV dosyası kaydedildi: {output_path}")
