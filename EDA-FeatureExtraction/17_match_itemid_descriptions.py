import os

# 📂 Giriş dosyaları ve çıkış dosyaları
counts_paths = [
    "Sepsis-AI/output/microbio_itemid_usage_counts.txt",
    "Sepsis-AI/output/inputevents_itemid_usage_counts.txt",
    "Sepsis-AI/output/outputevents_itemid_usage_counts.txt"
]

descriptions_path = "sepsis_keyword_matches.txt"
output_path = "Sepsis-AI/output/matched_itemids_with_descriptions_ALL.txt"

# 🔢 Tüm count'ları birleştir
itemid_counts = {}
for path in counts_paths:
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                itemid, count = map(str.strip, line.strip().split(":"))
                itemid_counts[itemid] = int(count)

# 🔍 Açıklamaları eşleştir
matched_lines = {}
with open(descriptions_path, "r", encoding="utf-8") as desc_file:
    for line in desc_file:
        if line.strip() == "" or "Anahtar Kelime" in line:
            continue
        itemid = line.strip().split(",")[0]
        if itemid in itemid_counts and itemid not in matched_lines:
            count = itemid_counts[itemid]
            matched_lines[itemid] = (count, line.strip())

# 📊 Count'a göre azalan sırala
sorted_lines = sorted(matched_lines.items(), key=lambda x: x[1][0], reverse=True)

# 💾 Dosyaya yaz
with open(output_path, "w", encoding="utf-8") as out:
    for itemid, (count, desc) in sorted_lines:
        out.write(f"{itemid}: {count} | {desc}\n")

print(f"✅ Sonuç dosyası oluşturuldu: {output_path}")
