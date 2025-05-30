import streamlit as st
import base64
import requests
import sqlite3
from PIL import Image

# Lire l'image et l'encoder en base64
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Logo encodé
logo_base64 = get_base64_image("./images/ensat.png")

st.set_page_config(page_title="Scanner System", layout="wide")

# Init
query_params = st.query_params
page = query_params.get("page", "Accueil")


# CSS
st.markdown("""
    <style>
        header { visibility: hidden; }
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 999;
            background-color: #ffffff;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 30px;
            box-shadow: 0 2px 8px rgba(50, 127, 251, 0.2);
            width: 100%;
        }
        .nav-left { display: flex; align-items: center; }
        .nav-left img { height: 40px; margin-right: 15px; }
        .nav-buttons button {
            margin-right: 10px;
            border-radius: 8px;
            background-color: white;
            border: none;
            box-shadow: 0 2px 8px rgba(50, 127, 251, 0.2);
            color: black;
            padding: 7px 22px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            font-weight: bold;
            transition: background-color 0.3s, color 0.3s;
            cursor: pointer;
        }
        .nav-buttons button:hover {
            background-color: #0a43a2;
            color: white;
            box-shadow: 0 2px 8px rgba(50, 127, 251, 0.2);
        }
        .main-content { padding-top: 140px; }
        .footer {
            text-align: center;
            font-size: 0.85rem;
            color: #888;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ccc;
        }
    </style>
""", unsafe_allow_html=True)

# Fonction pour récupérer les niveaux
def get_niveaux():
    conn = sqlite3.connect("./db/scannerSYS.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nom_niveau FROM niveau ORDER BY nom_niveau")
    niveaux = [row[0] for row in cursor.fetchall()]
    conn.close()
    return niveaux

niveaux = get_niveaux()


st.markdown(f"""
<div class="navbar">
    <div class="nav-left">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo">
        <h3 style="margin: 0; color: #0a43a2;">ScannerSystem</h3>
    </div>
    <div class="nav-buttons">
        <form method="get" action="/" style="display:inline;">
            <input type="hidden" name="page" value="Accueil"/>
            <button type="submit">Accueil</button>
        </form>
        <form method="get" action="/" style="display:inline;">
            <input type="hidden" name="page" value="Présence"/>
            <button type="submit">Présence</button>
        </form>
        <form method="get" action="/" style="display:inline;">
            <input type="hidden" name="page" value="PDF"/>
            <button type="submit">PdfGeneratorScan</button>
        </form>
        <form method="get" action="/" style="display:inline;">
            <input type="hidden" name="page" value="Excel"/>
            <button type="submit">ExcelGeneratorScan</button>
        </form>
        <form method="get" action="/" style="display:inline;">
            <input type="hidden" name="page" value="TP"/>
            <button type="submit">TpListGenerator</button>
        </form>
    </div>
</div>
""", unsafe_allow_html=True)


# Affichage des pages dynamiques
if page == "Accueil":
    st.markdown("""
        <style>
            .main-title {
                font-size: 38px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 15px;
            }
            .subtitle {
                font-size: 22px;
                color: #1f4e79;
                margin-top: 25px;
                margin-bottom: 10px;
            }
            .description {
                font-size: 17px;
                color: #444;
                line-height: 1.6;
                margin-bottom: 25px;
            }
            .feature-list {
                background-color: #f7f9fc;
                padding: 20px 25px;
                border-radius: 8px;
                border-left: 6px solid #1f4e79;
                list-style-type: square;
            }
            .feature-list li {
                margin-bottom: 12px;
                font-size: 16px;
                color: #333;
            }
            .footer-note {
                font-size: 14px;
                color: #777;
                margin-top: 40px;
                font-style: italic;
            }
        </style>

        <div class="main-title">Scanner System – Plateforme pour les enseignants de l’ENSAT</div>

        <div class="description">
            Cette application a été spécifiquement conçue pour répondre aux besoins des professeurs de l’École Nationale des Sciences Appliquées de Tanger (ENSAT).
            Elle vise à <strong>automatiser les tâches répétitives</strong> liées à la gestion pédagogique, afin de gagner du temps, améliorer l'organisation des cours et garantir un meilleur suivi des étudiants.
        </div>

        <div class="subtitle">Fonctionnalités principales</div>
        <ul class="feature-list">
            <li>Générer automatiquement des feuilles de présence vierges personnalisées par classe et par nombre de séances</li>
            <li>Scanner les feuilles de présence signées et en extraire les données vers Excel ou PDF</li>
            <li>Suivi automatique de l’assiduité et génération de rapports par étudiant</li>
            <li>Répartition personnalisée des groupes pour les travaux pratiques (TP)</li>
            <li>Organisation simplifiée des listes de TP et exportation rapide</li>
        </ul>

        <div class="footer-note">
            Utilisez le menu au dessus pour accéder aux différentes fonctionnalités. Ce système évolue en fonction des retours des enseignants de l’ENSAT.
        </div>
    """, unsafe_allow_html=True)


if page == "Présence":
    st.subheader("📝 Générer une feuille de présence PDF")
    niveau_presence = st.selectbox("📘 Choisissez le niveau", niveaux, key="niveau_presence")
    nb_seances = st.number_input("📆 Nombre de séances", min_value=1, max_value=30, value=6, step=1, key="nb_seances_presence")
    if st.button("📄 Générer la feuille de présence", key="btn_presence"):
        with st.spinner("Génération..."):
            response = requests.post("http://127.0.0.1:5000/generate_presence", json={
                "niveau": niveau_presence,
                "nb_seances": nb_seances
            })
            if response.status_code == 200:
                st.success("✅ PDF généré !")
                st.download_button("📥 Télécharger", response.content, file_name=f"{niveau_presence}_presence.pdf", mime="application/pdf")
            else:
                st.error("❌ Erreur : " + response.json().get("error", "Erreur inconnue"))

if page == "PDF":
    st.subheader("📄 Génération PDF aligné à partir d'une image")
    uploaded_pdf = st.file_uploader("📤 Dépose ton image", type=["jpg", "jpeg", "png"], key="pdf_upload")
    if uploaded_pdf and st.button("📄 Générer le fichier PDF", key="btn_pdf"):
        with st.spinner("Envoi au serveur..."):
            files = {'file': (uploaded_pdf.name, uploaded_pdf, uploaded_pdf.type)}
            response = requests.post("http://127.0.0.1:5000/to_pdf", files=files)
            if response.status_code == 200:
                st.success("✅ PDF généré !")
                st.download_button("📥 Télécharger", response.content, file_name="document_aligne.pdf", mime="application/pdf")
            else:
                st.error("❌ Erreur : " + response.json().get("error", "Erreur inconnue"))

if page == "Excel":
    st.subheader("🧠 Image ➝ Excel")
    uploaded_excel = st.file_uploader("📤 Uploade ton image", type=["jpg", "jpeg", "png"], key="excel_upload")
    if uploaded_excel and st.button("🧠 Générer le fichier Excel", key="btn_excel"):
        with st.spinner("Envoi au serveur..."):
            files = {'file': (uploaded_excel.name, uploaded_excel, uploaded_excel.type)}
            response = requests.post("http://127.0.0.1:5000/convert", files=files)
            if response.status_code == 200:
                st.success("✅ Excel généré !")
                st.download_button("📥 Télécharger", response.content, file_name="tableau.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.error("❌ Erreur : " + response.json().get("error", "Erreur inconnue"))

if page == "TP":
    st.subheader("👥 Générateur de binômes")
    niveau_binome = st.selectbox("🏷️ Choisissez le niveau", niveaux, key="niveau_binome")
    taille_groupe = st.number_input("👥 Taille du groupe", min_value=2, max_value=10, value=2, step=1, key="taille_groupe_binomes")
    if st.button("📄 Générer binômes PDF + Excel", key="btn_binomes"):
        with st.spinner("Génération..."):
            response = requests.post("http://127.0.0.1:5000/generate_binomes", json={
                "niveau": niveau_binome,
                "taille_groupe": taille_groupe
            })
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Binômes générés !")
                with open(data["pdf"], "rb") as f:
                    st.download_button("📄 Télécharger PDF", f.read(), file_name=f"Groupes_{niveau_binome}.pdf", mime="application/pdf")
                with open(data["excel"], "rb") as f:
                    st.download_button("📊 Télécharger Excel", f.read(), file_name=f"Groupes_{niveau_binome}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.error("❌ " + response.json().get("error", "Erreur inconnue"))

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    © 2025 Scanner System. Tous droits réservés.
</div>
""", unsafe_allow_html=True)