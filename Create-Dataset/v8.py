import pandas as pd

# === Dosya yolu ===
path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered.csv"
df = pd.read_csv(path)

# === Eksik veri sayısı hesapla ===
df["missing_count"] = df.isnull().sum(axis=1)

# === Duplicate kombinasyonları bul ===
dupes = df.groupby(["subject_id", "hadm_id"]).size().reset_index(name="count")
dupes = dupes[dupes["count"] > 1]

# === Duplicate grupların boşluk analizi ===
dupe_missing_summary = (
    df.groupby(["subject_id", "hadm_id"])
    .agg(
        tekrar_sayisi=("stay_id", "count"),
        min_bos=("missing_count", "min"),
        max_bos=("missing_count", "max"),
        mean_bos=("missing_count", "mean")
    )
    .reset_index()
)
dupe_missing_summary = dupe_missing_summary[dupe_missing_summary["tekrar_sayisi"] > 1]

# === En çok boşluğu olan ilk 10 satır ===
top_missing = df.sort_values(by="missing_count", ascending=False)[["subject_id", "hadm_id", "stay_id", "missing_count"]].head(10)

# === Boşluk dağılımı ===
bins = [0, 10, 20, 50, 100, df["missing_count"].max()]
labels = ["0-10", "10-20", "20-50", "50-100", "100+"]
df["missing_bin"] = pd.cut(df["missing_count"], bins=bins, labels=labels, right=False)
missing_dist = df["missing_bin"].value_counts().sort_index()

# === Sonuçları yazdır ===
print("\n=== Duplicate subject_id + hadm_id kombinasyonları ===")
print(dupe_missing_summary.to_string(index=False))

print("\n=== En çok boşluğu olan ilk 10 satır ===")
print(top_missing.to_string(index=False))

print("\n=== Boşluk dağılımı ===")
for bin_label, count in missing_dist.items():
    print(f"{bin_label}: {count} satır")
