import os
import pandas as pd
import random

# Çıktı dosyası
output_file = "dataset_structure_summary.txt"

# Ana klasörler
directories = ["raw/hosp", "raw/icu"]

with open(output_file, "w", encoding="utf-8") as f:
    for folder in directories:
        for file in os.listdir(folder):
            if file.endswith(".csv"):
                path = os.path.join(folder, file)
                f.write(f"\n{'='*80}\n")
                f.write(f"📄 Dosya: {path}\n")
                try:
                    # Sadece ilk 1000 satırı oku (sütunları tanımak ve veri tipi almak için yeterli)
                    df = pd.read_csv(path, nrows=1000, low_memory=False)

                    f.write(f"📊 Toplam Sütun Sayısı: {len(df.columns)}\n")
                    f.write(f"🧩 Sütun İsimleri: {list(df.columns)}\n")
                    f.write(f"📐 Veri Tipleri:\n{df.dtypes}\n\n")

                    # Toplam satır sayısını sadece başlıkla okuyarak bul
                    total_rows = sum(1 for _ in open(path, encoding="utf-8")) - 1
                    f.write(f"📈 Toplam Satır Sayısı (yaklaşık): {total_rows}\n")

                    # Boşluğu en az olan sütunları seç ve shuffle yap
                    non_null_cols = df.isnull().sum().sort_values()
                    top_cols = non_null_cols[non_null_cols <= 3].index.tolist()
                    if top_cols:
                        sampled = df[top_cols].dropna().sample(n=min(5, len(df)), random_state=42)
                        f.write("🎲 Rastgele 5 Satır (boşluğu en az olan sütunlardan):\n")
                        f.write(sampled.to_string(index=False))
                    else:
                        sampled = df.sample(n=min(5, len(df)), random_state=42)
                        f.write("🎲 Rastgele 5 Satır:\n")
                        f.write(sampled.to_string(index=False))

                    f.write("\n\n")
                except Exception as e:
                    f.write(f"❌ Hata: {e}\n\n")

print(f"\n✅ İşlem tamamlandı. Sonuçlar '{output_file}' dosyasına yazıldı.")
