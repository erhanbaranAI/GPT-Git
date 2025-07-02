import pandas as pd

def analyze_large_csv(path, name, chunksize=100_000):
    print(f"🔍 {name} inceleniyor...")
    total_rows = 0
    example_rows = []

    for chunk in pd.read_csv(path, chunksize=chunksize):
        total_rows += len(chunk)
        
        full_rows = chunk.dropna()
        for i in range(len(full_rows)):
            if len(example_rows) >= 3:
                break
            example_rows.append(full_rows.iloc[i])

        if len(example_rows) >= 3:
            break

    # Tek bir chunk ile sütun bilgisi al
    cols = pd.read_csv(path, nrows=1).columns.tolist()
    print(f"📄 {name} - Sütun Sayısı:", len(cols))
    print(f"🧩 {name} - Sütunlar:", cols)
    print(f"🔢 {name} - Toplam Satır Sayısı:", total_rows)
    print(f"🎲 {name} - Rastgele 3 Dolu Satır:")
    for i, row in enumerate(example_rows):
        print(f"  {i+1}.", row.to_dict())
    print("-" * 60)

# 🔍 İnceleme işlemi başlatılıyor
analyze_large_csv("Sepsis-AI/processed/chart_sepsis.csv", "Sepsis")
analyze_large_csv("Sepsis-AI/processed/chart_nonsepsis.csv", "Non-Sepsis")
