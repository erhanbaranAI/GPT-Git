import pandas as pd
import numpy as np
from datetime import timedelta
from functools import reduce

# === PATHLER ===
sepsis_patients_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\filtered_data\icu_sepsis_filtered.csv"
lab_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\raw\hosp\labevents.csv"
chart_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\raw\icu\chartevents.csv"
output_path = r"C:\Users\lerha\OneDrive\Masaüstü\All-in-Celsus\Sepsis-AI\Dataset\final_dataset_filtered.csv"

# === SEPSİSLİ HASTALAR ===
sepsis_df = pd.read_csv(sepsis_patients_path)
sepsis_keys_lab = sepsis_df[["subject_id", "hadm_id"]]
sepsis_keys_chart = sepsis_df[["subject_id", "hadm_id", "stay_id"]]

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

# === DATA OKUMA ===
def read_events(path, ids, merge_keys, join_cols, chunksize=1_000_000):
    data = []
    cols = join_cols + ["itemid", "charttime", "valuenum"]
    for chunk in pd.read_csv(path, usecols=cols, chunksize=chunksize):
        chunk = chunk[chunk["itemid"].isin(ids)]
        chunk = pd.merge(chunk, merge_keys, on=join_cols, how="inner")
        chunk["charttime"] = pd.to_datetime(chunk["charttime"])
        data.append(chunk)
    return pd.concat(data, ignore_index=True)

print("🔹 LAB yükleniyor...")
lab_df = read_events(lab_path, [v["lab"] for v in pair_itemids.values()] + other_lab_itemids, sepsis_keys_lab, ["subject_id", "hadm_id"])

print("🔹 CHART yükleniyor...")
chart_df = read_events(chart_path, [v["chart"] for v in pair_itemids.values()] + other_chart_itemids + list(temperature_ids.values()), sepsis_keys_chart, ["subject_id", "hadm_id", "stay_id"])

# === Sıcaklık ===
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

# === Pair işleme ===
def merge_pairs(lab_id, chart_id):
    lab = lab_df[lab_df["itemid"] == lab_id]
    chart = chart_df[chart_df["itemid"] == chart_id]
    final = []
    for key, l_grp in lab.groupby(["subject_id", "hadm_id"]):
        c_grp = chart[(chart["subject_id"] == key[0]) & (chart["hadm_id"] == key[1])]
        # matched olanları at, kalanları ekle
        merged_lab = l_grp.copy()
        for _, l_row in l_grp.iterrows():
            matched = c_grp[
                (c_grp["charttime"] >= l_row["charttime"] - timedelta(days=1)) &
                (c_grp["charttime"] <= l_row["charttime"] + timedelta(days=1)) &
                (np.isclose(c_grp["valuenum"], l_row["valuenum"], atol=0.01))
            ]
            if not matched.empty:
                merged_lab = merged_lab.drop(l_row.name)
        final.append(pd.concat([merged_lab, c_grp], ignore_index=True))
    if final:
        return pd.concat(final, ignore_index=True)
    return pd.DataFrame()

# === İstatistik ===
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

# === Çalıştır ===
features = []

for name, ids in pair_itemids.items():
    merged = merge_pairs(ids["lab"], ids["chart"])
    features.append(compute_agg(merged, name))

for item in other_lab_itemids:
    df = lab_df[lab_df["itemid"] == item]
    features.append(compute_agg(df, f"ID{item}"))

for item in other_chart_itemids:
    df = chart_df[chart_df["itemid"] == item]
    features.append(compute_agg(df, f"ID{item}"))

if not temp_df.empty:
    features.append(compute_agg(temp_df, "Temperature"))

# === Birleştir ve Kaydet ===
final_df = reduce(lambda l, r: pd.merge(l, r, on=list(set(l.columns).intersection(set(r.columns))), how="outer"), features)
final_df.to_csv(output_path, index=False)

print(f"✅ Dataset oluşturuldu: {output_path}")
print(f"Toplam kayıt: {final_df.shape[0]}")
