import pandas as pd
import numpy as np
from collections import defaultdict

# Ayarlar
chunk_size = 500_000
paths = {
    "sepsis": "Sepsis-AI/processed/chart_sepsis.csv",
    "nonsepsis": "Sepsis-AI/processed/chart_nonsepsis.csv"
}

def compute_stats(path, prefix):
    value_store = defaultdict(list)  # Her itemid için valuenum listesi
    total_counts = defaultdict(int)  # itemid -> toplam veri sayısı
    null_counts = defaultdict(int)   # itemid -> boş veri sayısı

    for chunk in pd.read_csv(path, usecols=["itemid", "valuenum"], chunksize=chunk_size):
        chunk["valuenum"] = pd.to_numeric(chunk["valuenum"], errors='coerce')  # NaN'ları yakala
        grouped = chunk.groupby("itemid")

        for itemid, group in grouped:
            total = len(group)
            nulls = group["valuenum"].isna().sum()
            non_null_values = group["valuenum"].dropna().tolist()

            total_counts[itemid] += total
            null_counts[itemid] += nulls
            value_store[itemid].extend(non_null_values)


    # İstatistikleri hesapla
    rows = []
    for itemid, values in value_store.items():
        if not values:
            continue
        values_np = np.array(values)
        rows.append({
            "itemid": itemid,
            f"{prefix}_count": len(values_np),
            f"{prefix}_null_count": null_counts[itemid],
            f"{prefix}_mean": np.mean(values_np),
            f"{prefix}_median": np.median(values_np),
            f"{prefix}_std": np.std(values_np),
            f"{prefix}_min": np.min(values_np),
            f"{prefix}_max": np.max(values_np),
        })

    return pd.DataFrame(rows)

# ✅ İşlemler
df_sepsis = compute_stats(paths["sepsis"], "sepsis")
df_nonsepsis = compute_stats(paths["nonsepsis"], "nonsepsis")

# ✅ Birleştir ve eksik doldur
df = pd.merge(df_sepsis, df_nonsepsis, on="itemid", how="outer").fillna(0)

# ✅ Fark kolonlarını ekle
df["mean_diff"] = df["sepsis_mean"] - df["nonsepsis_mean"]
df["sepsis_missing_ratio"] = df["sepsis_null_count"] / (df["sepsis_count"] + df["sepsis_null_count"])
df["nonsepsis_missing_ratio"] = df["nonsepsis_null_count"] / (df["nonsepsis_count"] + df["nonsepsis_null_count"])

# ✅ Kaydet
output_path = "Sepsis-AI/output/itemid_detailed_stats.csv"
df.to_csv(output_path, index=False)
print(f"✅ Tüm istatistikler doğru hesaplandı ve kaydedildi: {output_path}")
