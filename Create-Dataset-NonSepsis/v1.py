import pandas as pd
import numpy as np
from datetime import timedelta
from functools import reduce

# === PATHLER ===
sepsis_patients_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\filtered_data\icu_sepsis_filtered.csv"
lab_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\raw\hosp\labevents.csv"
chart_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\raw\icu\chartevents.csv"
output_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\non_sepsis_dataset.csv"

# === SEPSİS SUBJECT_ID LİSTESİ ===
sepsis_df = pd.read_csv(sepsis_patients_path)
sepsis_subjects = sepsis_df['subject_id'].unique()

# === ITEM TANIMLARI ===
pair_itemids = {
    "WBC": {"lab": 51301, "chart": 220546},
    "Creatinine": {"lab": 50912, "chart": 220615},
    "Platelet": {"lab": 51265, "chart": 227457},
    "BaseExcess": {"lab": 50802, "chart": 224828},
    "BilirubinTotal": {"lab": 50885, "chart": 225690},
    "Glucose": {"lab": 50931, "chart": 220621}
}
temperature_ids = {"Fahrenheit": 223761, "Celsius": 223762}
other_chart_itemids = [225664, 225624, 227443, 223830, 220277, 220227, 220224, 220235, 220045, 220210, 224689]
other_lab_itemids = [50813, 50817, 50821, 50818]

all_itemids = [v["lab"] for v in pair_itemids.values()] + \
              [v["chart"] for v in pair_itemids.values()] + \
              list(temperature_ids.values()) + other_chart_itemids + other_lab_itemids

# === VERİ OKUMA ===
def read_events(path, is_chart=False, chunksize=1_000_000):
    cols = ["subject_id", "hadm_id", "itemid", "charttime", "valuenum"]
    if is_chart:
        cols.insert(2, "stay_id")
    data = []
    for chunk in pd.read_csv(path, usecols=cols, chunksize=chunksize):
        chunk = chunk[~chunk["subject_id"].isin(sepsis_subjects)]
        chunk = chunk[chunk["itemid"].isin(all_itemids)]
        chunk["charttime"] = pd.to_datetime(chunk["charttime"])
        data.append(chunk)
    return pd.concat(data, ignore_index=True)

print("🔹 LAB yükleniyor...")
lab_df = read_events(lab_path, is_chart=False)

print("🔹 CHART yükleniyor...")
chart_df = read_events(chart_path, is_chart=True)

# === TEMP İŞLE ===
def process_temp(df):
    temp = df[df["itemid"].isin(temperature_ids.values())]
    rows = []
    for _, grp in temp.groupby(["subject_id", "hadm_id", "stay_id", "charttime"]):
        f = grp[grp["itemid"] == temperature_ids["Fahrenheit"]]
        c = grp[grp["itemid"] == temperature_ids["Celsius"]]
        if not f.empty:
            rows.append(f.iloc[0])
        elif not c.empty:
            row = c.iloc[0].copy()
            row["valuenum"] = row["valuenum"] * 9/5 + 32
            rows.append(row)
    return pd.DataFrame(rows)

temp_df = process_temp(chart_df)

# === AGG ===
def compute_agg(df, name):
    if df.empty:
        return pd.DataFrame()
    group_cols = [col for col in ["subject_id", "hadm_id", "stay_id"] if col in df.columns]
    agg = df.groupby(group_cols)["valuenum"].agg(
        mean="mean", min="min", max="max", std="std",
        first=lambda x: x.iloc[0], last=lambda x: x.iloc[-1]
    ).reset_index()
    agg[f"{name}_diff"] = agg["max"] - agg["min"]
    rename = {col: f"{name}_{col}" for col in ["mean", "min", "max", "std", "first", "last"]}
    agg = agg.rename(columns=rename)
    return agg

# === ÇALIŞTIR ===
features = []

for name, ids in pair_itemids.items():
    lab_part = lab_df[lab_df["itemid"] == ids["lab"]]
    chart_part = chart_df[chart_df["itemid"] == ids["chart"]]
    combined = pd.concat([lab_part, chart_part], ignore_index=True)
    features.append(compute_agg(combined, name))

for item in other_lab_itemids:
    df = lab_df[lab_df["itemid"] == item]
    features.append(compute_agg(df, f"ID{item}"))

for item in other_chart_itemids:
    df = chart_df[chart_df["itemid"] == item]
    features.append(compute_agg(df, f"ID{item}"))

if not temp_df.empty:
    features.append(compute_agg(temp_df, "Temperature"))

# === BİRLEŞTİR ===
from functools import reduce
final_df = reduce(lambda l, r: pd.merge(l, r, on=list(set(l.columns).intersection(set(r.columns))), how="outer"), features)

# Boşluk oranını hesapla ve %50'den az boşluğu olanları al
final_df["missing_count_row"] = final_df.isnull().sum(axis=1)
final_df["total_cols"] = final_df.shape[1]
final_df["missing_ratio"] = final_df["missing_count_row"] / final_df["total_cols"]
final_df = final_df[final_df["missing_ratio"] < 0.5]

# 10k sınırı
final_df = final_df.sample(n=10000, random_state=42) if len(final_df) > 10000 else final_df

# === KAYDET ===
final_df.to_csv(output_path, index=False)
print(f"✅ Non-sepsis dataset oluşturuldu ve kaydedildi: {output_path}")
print(f"Toplam kayıt sayısı: {final_df.shape[0]}")
