from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'  # Dossier où les fichiers uploadés seront stockés

# Assurez-vous que le dossier d'uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Fonction pour charger les données du fichier Excel
def charger_donnees_excel(fichier=None):
    if fichier:
        # Charger le fichier uploadé
        data = pd.read_excel(fichier)
    else:
        # Charger un fichier par défaut si aucun fichier n'est uploadé
        data = pd.read_excel("contacts_ameli.xlsx")
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Vérifier si un fichier a été uploadé
        if 'file' not in request.files:
            return redirect(request.url)
        
        fichier = request.files['file']
        
        # Vérifier si le fichier est bien sélectionné et s'il est Excel
        if fichier and fichier.filename.endswith(('.xlsx', '.xls')):
            chemin_fichier = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(fichier.filename))
            fichier.save(chemin_fichier)
            
            # Charger les données du fichier uploadé
            contacts = charger_donnees_excel(chemin_fichier).to_dict(orient="records")
            
            # Supprimer le fichier après chargement (facultatif, pour nettoyer les uploads)
            os.remove(chemin_fichier)
        else:
            # Charger le fichier par défaut si aucun fichier valide n'est uploadé
            contacts = charger_donnees_excel().to_dict(orient="records")
    else:
        # Charger le fichier par défaut si la méthode est GET
        contacts = charger_donnees_excel().to_dict(orient="records")

    return render_template('index.html', contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)
