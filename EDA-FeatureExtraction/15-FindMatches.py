# Dosya yolları
counts_path = "Sepsis-AI/output/inputevents_itemid_usage_counts.txt"
descriptions_path = "sepsis_keyword_matchesv2.txt"
output_path = "Sepsis-AI/output/matched_itemid_with_descriptions_inputevents.txt"

# 1. itemid: count sözlüğünü oluştur
itemid_counts = {}
with open(counts_path, "r", encoding="utf-8") as f:
    for line in f:
        if ":" in line:
            parts = line.strip().split(":")
            itemid = parts[0].strip()
            count = int(parts[1].strip())
            itemid_counts[itemid] = count

# 2. Açıklama satırlarını topla (sadece eşleşenler, tekrarsız)
matched_lines = {}
with open(descriptions_path, "r", encoding="utf-8") as desc_file:
    for line in desc_file:
        if line.strip() == "" or "Anahtar Kelime" in line:
            continue  # başlık ve boş satırları atla
        itemid = line.strip().split(",")[0]
        if itemid in itemid_counts and itemid not in matched_lines:
            count = itemid_counts[itemid]
            matched_lines[itemid] = (count, line.strip())

# 3. Count'a göre azalan sıralama yap
sorted_lines = sorted(matched_lines.items(), key=lambda x: x[1][0], reverse=True)

# 4. Dosyaya yaz
with open(output_path, "w", encoding="utf-8") as out_file:
    for itemid, (count, desc) in sorted_lines:
        out_file.write(f"{itemid}: {count} | {desc}\n")
