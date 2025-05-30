from flask import Flask, request, send_file, jsonify
import sys
import os
sys.path.append(os.path.dirname(__file__))
from Controllers.presence_pdf import generer_feuille_presence
from Controllers.table_scanner import image_to_excel
from Controllers.images_to_pdf import image_to_aligned_pdf
from Controllers.dynamiqueGroupList import generate_binomes_from_db

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_image_to_excel():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier'}), 400

    file = request.files['file']
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    filename_wo_ext = os.path.splitext(file.filename)[0]
    output_path = os.path.join(OUTPUT_FOLDER, f"{filename_wo_ext}.xlsx")

    try:
        result_path = image_to_excel(image_path, output_path)
        return send_file(result_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/to_pdf", methods=["POST"])
def convert_image_to_pdf():
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier fourni"}), 400

    file = request.files["file"]
    image_path = os.path.join("uploads", file.filename)
    file.save(image_path)

    filename_wo_ext = os.path.splitext(file.filename)[0]
    output_pdf = os.path.join("outputs", f"{filename_wo_ext}.pdf")

    try:
        result = image_to_aligned_pdf(image_path, output_pdf)
        return send_file(result, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/generate_presence", methods=["POST"])
def generate_presence_route():
    data = request.json
    niveau = data.get("niveau")  # ✅ Corrigé ici
    nb_seances = data.get("nb_seances", 6)

    if not niveau:
        return jsonify({"error": "Niveau manquant"}), 400

    try:
        pdf_path = generer_feuille_presence(niveau=niveau, nb_seances=nb_seances)
        return send_file(pdf_path, as_attachment=True)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate_binomes", methods=["POST"])
def generate_binomes_route():
    data = request.json
    niveau = data.get("niveau")
    taille_groupe = int(data.get("taille_groupe", 2))

    if not niveau:
        return jsonify({"error": "Niveau manquant"}), 400

    try:
        excel_path, pdf_path = generate_binomes_from_db(niveau_nom=niveau, taille_groupe=taille_groupe)
        return jsonify({"excel": excel_path, "pdf": pdf_path})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
