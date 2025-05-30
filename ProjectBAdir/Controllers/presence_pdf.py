from fpdf import FPDF
import sqlite3
import os

def generer_feuille_presence(niveau: str, nb_seances: int, db_path="./db/scannerSYS.db", output_dir="outputs") -> str:
    os.makedirs(output_dir, exist_ok=True)

    # Connexion à la DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Étape 1 : récupérer id_niveau depuis nom_niveau
    cursor.execute("SELECT id_niveau FROM niveau WHERE nom_niveau = ?", (niveau,))
    niveau_row = cursor.fetchone()
    if not niveau_row:
        conn.close()
        raise ValueError(f"Niveau '{niveau}' introuvable.")

    id_niveau = niveau_row[0]

    # Étape 2 : récupérer les étudiants
    cursor.execute("SELECT code_apoge, nom, prenom FROM etudiant WHERE id_niveau = ?", (id_niveau,))
    etudiants = cursor.fetchall()
    conn.close()

    if not etudiants:
        raise ValueError("Aucun étudiant trouvé pour le niveau spécifié.")

    # Génération PDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Feuille de présence - {niveau}", ln=True, align="C")
    pdf.ln(5)

    headers = ["Code Apogée", "Nom", "Prénom"] + [f"Séance {i+1}" for i in range(nb_seances)]
    col_widths = [30, 40, 40] + [25] * nb_seances
    row_height = 5

    pdf.set_font("Arial", "B", 10)
    for header, width in zip(headers, col_widths):
        pdf.cell(width, row_height, header, border=1, align="C")
    pdf.ln()

    pdf.set_font("Arial", "", 10)
    for etu in etudiants:
        row = list(etu) + [""] * nb_seances
        for val, width in zip(row, col_widths):
            pdf.cell(width, row_height, str(val), border=1)
        pdf.ln()

    file_path = os.path.join(output_dir, f"{niveau}_presence.pdf")
    pdf.output(file_path)

    return file_path
