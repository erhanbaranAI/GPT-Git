import pandas as pd

# CSV dosyasını yükle (yalnızca itemid kolonu okunur)
df = pd.read_csv("Sepsis-AI/output/icu_sepsis_labs.csv", usecols=["itemid"])

# itemid’leri say ve sırala
item_counts = df["itemid"].value_counts().reset_index()
item_counts.columns = ["itemid", "count"]

# TXT dosyasına yaz
with open("Sepsis-AI/output/itemid_usage_counts.txt", "w", encoding="utf-8") as f:
    for _, row in item_counts.iterrows():
        f.write(f"{int(row['itemid'])}: {int(row['count'])}\n")

print("✅ itemid kullanım sıklığı başarıyla yazıldı: Sepsis-AI/output/itemid_usage_counts.txt")


# import pandas as pd

# # CSV dosyasını yükle (yalnızca test_itemid kolonu okunur)
# df = pd.read_csv("Sepsis-AI/output/icu_sepsis_microbiologyevents.csv", usecols=["test_itemid"])

# # itemid’leri say ve sırala
# item_counts = df["test_itemid"].value_counts().reset_index()
# item_counts.columns = ["test_itemid", "count"]

# # TXT dosyasına yaz
# with open("Sepsis-AI/output/itemid_usage_counts_microbiologyevents.txt", "w", encoding="utf-8") as f:
#     for _, row in item_counts.iterrows():
#         f.write(f"{int(row['test_itemid'])}: {int(row['count'])}\n")

# print("✅ test_itemid kullanım sıklığı başarıyla yazıldı: Sepsis-AI/output/itemid_usage_counts_microbiologyevents.txt")