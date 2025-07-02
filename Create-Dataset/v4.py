import pandas as pd

# === VERİYİ YÜKLE ===
path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered.csv"
df = pd.read_csv(path)

# === EKSİK VERİ ORANLARI ===
missing = df.isnull().mean() * 100
missing = missing[missing > 0].sort_values(ascending=False)

# === EKRANA YAZMA ===
print("🔎 Eksik Veri Oranları (%):")
print(missing)

# === DOSYAYA KAYDET ===
output_txt_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\missing_report.txt"
with open(output_txt_path, "w") as f:
    f.write("Eksik Veri Oranları (%)\n")
    f.write(missing.to_string())

print(f"✅ Eksik veri oranları şuraya kaydedildi: {output_txt_path}")
