import os
import cv2
import pandas as pd
from paddleocr import PaddleOCR

# Initialiser l’OCR une seule fois (optimisé pour réutilisation)
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

def image_to_excel(image_path: str, output_path: str) -> str:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image introuvable : {image_path}")

    # OCR
    result = ocr.ocr(image_path, cls=True)

    # Extraire les textes + coordonnées
    entries = []
    for line in result[0]:
        box = line[0]
        text = line[1][0]
        x = min(pt[0] for pt in box)
        y = min(pt[1] for pt in box)
        entries.append({'text': text.strip(), 'x': x, 'y': y})

    # Grouper et trier les lignes
    lines = group_by_y(entries)
    table = []
    for line in lines:
        sorted_line = sorted(line, key=lambda e: e['x'])
        row = [cell['text'] for cell in sorted_line]
        table.append(row)

    # Uniformiser
    max_cols = max(len(row) for row in table)
    table = [row + [""] * (max_cols - len(row)) for row in table]

    # Export Excel
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.DataFrame(table)
    df.to_excel(output_path, index=False, header=False)

    print(f"✅ Export terminé : {output_path}")
    return output_path
