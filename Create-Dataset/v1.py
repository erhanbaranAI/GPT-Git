import pandas as pd
import os

# === Ayarlar ===
base_path = "raw"
output_path = "Sepsis-AI/outputCD"
os.makedirs(output_path, exist_ok=True)

target_subject_id = 10001843
target_hadm_id = 26133978
target_stay_id = 39698942
chunksize = 1_000_000  # Ayarlanabilir

# === Hedef itemid'ler ===
features = {
    "lab": {
        "file": f"{base_path}/hosp/labevents.csv",
        "itemids": [51301, 50813, 50931, 50912, 50885, 51265, 50802, 50817, 50821, 50818],
        "filter_on": ["subject_id", "hadm_id", "itemid"],
        "filter_values": [target_subject_id, target_hadm_id]
    },
    "chart": {
        "file": f"{base_path}/icu/chartevents.csv",
        "itemids": [
            220546, 225664, 220621, 220615, 225690, 227457, 225624,
            227443, 224828, 223830, 220277, 220227, 220224, 220235,
            220045, 220210, 224689, 223761, 223762
        ],
        "filter_on": ["subject_id", "stay_id", "itemid"],
        "filter_values": [target_subject_id, target_stay_id]
    },
    "output": {
        "file": f"{base_path}/icu/outputevents.csv",
        "itemids": [226559],
        "filter_on": ["subject_id", "stay_id", "itemid"],
        "filter_values": [target_subject_id, target_stay_id]
    },
    "input": {
        "file": f"{base_path}/icu/inputevents.csv",
        "itemids": [225158, 220949],
        "filter_on": ["subject_id", "stay_id", "itemid"],
        "filter_values": [target_subject_id, target_stay_id]
    },
    "microbio": {
        "file": f"{base_path}/hosp/microbiologyevents.csv",
        "itemids": [90046, 90039, 90201, 90268],
        "filter_on": ["subject_id", "hadm_id", "test_itemid"],
        "filter_values": [target_subject_id, target_hadm_id],
        "itemid_col": "test_itemid"
    }
}

# === Fonksiyon: chunked CSV filtreleme ===
def filter_csv_in_chunks(path, itemid_col, filter_cols, filter_vals, itemids, output_name):
    result = []
    for chunk in pd.read_csv(path, chunksize=chunksize):
        cond = (chunk[filter_cols[0]] == filter_vals[0])
        if len(filter_cols) > 1:
            cond &= (chunk[filter_cols[1]] == filter_vals[1])
        if len(filter_cols) > 2:
            cond &= (chunk[filter_cols[2]].isin(itemids))
        else:
            cond &= (chunk[itemid_col].isin(itemids))
        filtered = chunk[cond]
        if not filtered.empty:
            result.append(filtered)

    if result:
        df_final = pd.concat(result)
        df_final.to_csv(os.path.join(output_path, output_name), index=False)
        print(f"[✓] {output_name} kaydedildi: {len(df_final)} satır")
    else:
        print(f"[!] {output_name} için veri bulunamadı")

# === Tüm kategoriler için işle
for key, info in features.items():
    itemid_col = info.get("itemid_col", "itemid")
    filter_csv_in_chunks(
        path=info["file"],
        itemid_col=itemid_col,
        filter_cols=info["filter_on"],
        filter_vals=info["filter_values"],
        itemids=info["itemids"],
        output_name=f"{key}.csv"
    )
