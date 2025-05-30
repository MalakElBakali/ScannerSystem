import os
import cv2
import fitz  # PyMuPDF
from paddleocr import PaddleOCR

# Initialiser l’OCR une seule fois
ocr = PaddleOCR(use_angle_cls=True, lang='fr')

def image_to_aligned_pdf(image_path: str, output_path: str) -> str:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image introuvable : {image_path}")

    # Charger l’image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Impossible de lire l'image : {image_path}")
    height, width, _ = image.shape

    # OCR
    result = ocr.ocr(image_path, cls=True)

    # Créer le PDF
    doc = fitz.open()
    page = doc.new_page(width=width, height=height)

    for line in result[0]:
        box = line[0]
        text = line[1][0]

        x0 = min(pt[0] for pt in box)
        y0 = min(pt[1] for pt in box)
        box_height = max(pt[1] for pt in box) - min(pt[1] for pt in box)
        font_size = max(8, min(14, box_height * 0.8))

        page.insert_text(
            (x0, y0),
            text,
            fontsize=font_size,
            fontname="helv",
            color=(0, 0, 0)
        )

    # Sauvegarde
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    doc.close()

    print(f"✅ PDF aligné généré : {output_path}")
    return output_path
