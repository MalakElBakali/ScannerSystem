import os
import cv2
import pandas as pd
import numpy as np
from paddleocr import PaddleOCR

# Initialisation de l’OCR
ocr = PaddleOCR(use_angle_cls=True, lang='fr')

def group_by_y(entries, tolerance=15):
    entries = sorted(entries, key=lambda e: e['y'])
    groups = []
    current = []
    last_y = None
    for entry in entries:
        if last_y is None or abs(entry['y'] - last_y) < tolerance:
            current.append(entry)
        else:
            groups.append(current)
            current = [entry]
        last_y = entry['y']
    if current:
        groups.append(current)
    return groups

def is_signature_region(img_region, threshold=30):
    gray = cv2.cvtColor(img_region, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    density = np.sum(binary > 0) / binary.size * 100
    return density > threshold

def image_to_excel_with_signature_columns(image_path: str, output_path: str) -> str:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image introuvable : {image_path}")

    img = cv2.imread(image_path)
    result = ocr.ocr(image_path, cls=True)

    entries = []
    for line in result[0]:
        box = line[0]
        text = line[1][0]
        x = int(min(pt[0] for pt in box))
        y = int(min(pt[1] for pt in box))
        x_max = int(max(pt[0] for pt in box))
        y_max = int(max(pt[1] for pt in box))
        entries.append({'text': text.strip(), 'x': x, 'y': y, 'x_max': x_max, 'y_max': y_max})

    # Groupement par lignes
    lines = group_by_y(entries)
    table = []

    for line in lines:
        sorted_line = sorted(line, key=lambda e: e['x'])
        row = []
        for i, cell in enumerate(sorted_line):
            x1, y1, x2, y2 = cell['x'], cell['y'], cell['x_max'], cell['y_max']
            region = img[y1:y2, x1:x2]
            if len(row) < 3:
                # Colonnes Apogée, Nom, Prénom → OCR pur
                row.append(cell['text'])
            else:
                # Colonnes "Séance" → Signature = 1, sinon ""
                if is_signature_region(region):
                    row.append("1")
                else:
                    row.append("")
        table.append(row)

    # Normalisation
    max_cols = max(len(r) for r in table)
    table = [r + [""] * (max_cols - len(r)) for r in table]

    # Export Excel
    df = pd.DataFrame(table)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_excel(output_path, index=False, header=False)

    print(f"✅ Export terminé : {output_path}")
    return output_path

# === Point d'entrée ===
if __name__ == "__main__":
    image_to_excel_with_signature_columns(
        "./images/IimgScanne.jpg",
        "./outputs/presence_resultat.xlsx"
    )
