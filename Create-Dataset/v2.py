import pandas as pd

# Ortak LAB + CHART itemid çiftleri
itemid_pairs = {
    "WBC": {"lab": 51301, "chart": 220546},
    "Creatinine": {"lab": 50912, "chart": 220615},
    "Platelet": {"lab": 51265, "chart": 227457},
    "Base Excess": {"lab": 50802, "chart": 224828},
    "Bilirubin Total": {"lab": 50885, "chart": 225690},
    "Glucose": {"lab": 50931, "chart": 220621}
}

# Dosya yolları
lab_df = pd.read_csv("Sepsis-AI/outputCD/lab.csv")
chart_df = pd.read_csv("Sepsis-AI/outputCD/chart.csv")

# Her parametre için LAB vs CHART kıyası
for name, ids in itemid_pairs.items():
    print(f"\n=== {name} (LAB {ids['lab']} vs CHART {ids['chart']}) ===")
    
    # LAB ve CHART verileri
    lab_vals = lab_df[lab_df["itemid"] == ids["lab"]][["charttime", "valuenum"]]
    chart_vals = chart_df[chart_df["itemid"] == ids["chart"]][["charttime", "valuenum"]]
    
    # Merge zaman bazlı
    merged = pd.merge(lab_vals, chart_vals, on="charttime", suffixes=("_lab", "_chart"))
    
    if merged.empty:
        print("⚠ Eşleşen zaman bulunamadı.")
    else:
        for _, row in merged.iterrows():
            print(f"{row['charttime']}: LAB={row['valuenum_lab']} CHART={row['valuenum_chart']}")
