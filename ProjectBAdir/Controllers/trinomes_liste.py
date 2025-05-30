from paddleocr import PaddleOCR
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Border, Side
import os

# === PARAMÈTRES ===
img_path = "images/test1.jpg"  # ton image
output_path = "outputs/liste_etudiants_trinomes_styled.xlsx"
taille_groupe = 3  # change à 2 pour binôme, etc.

# === 1. OCR ===
ocr = PaddleOCR(use_angle_cls=True, lang='fr')
result = ocr.ocr(img_path, cls=True)

entries = []
for line in result[0]:
    box = line[0]
    text, conf = line[1]
    x = min(pt[0] for pt in box)
    y = min(pt[1] for pt in box)
    entries.append({'text': text.strip(), 'x': x, 'y': y})

# === 2. Groupement visuel (Y)
def group_by_y(entries, tolerance=15):
    sorted_entries = sorted(entries, key=lambda k: k['y'])
    groups = []
    current = []
    current_y = None
    for entry in sorted_entries:
        if current_y is None or abs(entry['y'] - current_y) < tolerance:
            current.append(entry)
        else:
            groups.append(current)
            current = [entry]
        current_y = entry['y']
    if current:
        groups.append(current)
    return groups

lines = group_by_y(entries)

# === 3. Trier et construire le tableau
table = []
for line in lines:
    sorted_line = sorted(line, key=lambda k: k['x'])
    table.append([cell['text'] for cell in sorted_line])

max_cols = max(len(row) for row in table)
table = [row + [""] * (max_cols - len(row)) for row in table]

# === 4. Ajouter la colonne "Groupe"
groupe_col = []
groupe_num = 1
for i in range(len(table)):
    if i % taille_groupe == taille_groupe - 1:
        groupe_col.append(f"G{groupe_num}")
        groupe_num += 1
    else:
        groupe_col.append("")

df = pd.DataFrame(table)
df.insert(0, "Groupe", groupe_col)

# Temp Excel file
temp_excel = "outputs/temp.xlsx"
os.makedirs("outputs", exist_ok=True)
df.to_excel(temp_excel, index=False, header=False)

# === 5. Stylisation avec bordure après chaque groupe
wb = load_workbook(temp_excel)
ws = wb.active

thick_border = Border(bottom=Side(border_style="thick", color="000000"))
# Taille du groupe (binôme=2, trinôme=3, etc.)
taille_groupe = 3

# Appliquer la bordure sur la dernière ligne de chaque groupe (saute l'en-tête)
for i in range(1 + taille_groupe, ws.max_row + 1, taille_groupe):
    for cell in ws[i]:
        cell.border = thick_border

# Save final styled Excel
wb.save(output_path)
os.remove(temp_excel)

print(f"✅ Fichier Excel généré avec style : {output_path}")
