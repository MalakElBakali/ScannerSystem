

## Étapes à suivre :

1. **Créer la base de données**
   - Aller dans le dossier `db/`
   - Lancer le fichier `create_db.py` pour créer la base :
     ```bash
     python create_db.py
     ```
   - Lancer les scripts d’insertion pour ajouter les données initiales.

   > (Optionnel) Vous pouvez utiliser **DB Browser for SQLite** pour visualiser la base de données.

2. **Lancer le backend**
   - Aller dans le dossier `Controllers/`
   - Lancer le fichier `route.py` :
     ```bash
     python route.py
     ```

3. **Lancer l’interface graphique**
   - Depuis le dossier `Controllers/`, lancer Streamlit :
     ```bash
     streamlit run app.py
     ```

## Installation des dépendances

Avant de commencer, installez les dépendances avec :

```bash
pip install -r requirements.txt
