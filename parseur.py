import os
import subprocess
import re

def parseur(fichier_pdf, dossier_sortie):
    if os.path.exists(fichier_pdf):
        nom_fichier = os.path.splitext(os.path.basename(fichier_pdf))[0]
        fichier_sortie = os.path.join(dossier_sortie, f"{nom_fichier}.txt")

        # Utilisation de pdftotext pour extraire le texte du PDF
        cmd = f"pdftotext '{fichier_pdf}' '{fichier_sortie}'"
        resultat = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if resultat.returncode == 0:
            with open(fichier_sortie, 'r') as fichier:
                texte = fichier.read()

            # Extraction du titre
            titre_match = re.match(r'^(.*?)\n', texte)
            titre = titre_match.group(1).replace(' ', '_') if titre_match else ""

            # Extraction de l'abstract
            correspondance_abstract = re.search(r'Abstract\n(.*?)(?:\s1\s|\sI\s|\sIntroduction\s|$)', texte, re.DOTALL)
            abstract = correspondance_abstract.group(1).replace('\n', ' ').strip() if correspondance_abstract else ""

            # Formatage des informations extraites
            informations_formatees = f"Nom du fichier d'origine : {nom_fichier}\n"
            informations_formatees += f"Titre du papier : {titre}\n"
            informations_formatees += f"Résumé de l'auteur (Abstract/Résumé) : {abstract}\n"

            # Informations dans le fichier de sortie
            open(fichier_sortie, 'w').close()
            with open(fichier_sortie, 'w') as fichier:
                fichier.write(informations_formatees)

        else:
            print(f"Erreur lors de l'extraction du texte : {resultat.stderr.decode('utf-8').strip()}")
    else:
        print(f"Le fichier PDF '{fichier_pdf}' n'existe pas.")

# Dossier contenant les fichiers PDF
dossier_pdf = '/home/nas-wks01/users/uapv2300275/ParseurScientifique/projet-parser/CORPUS_TRAIN'

# Dossier de sortie
dossier_sortie =  '/home/nas-wks01/users/uapv2300275/ParseurScientifique/projet-parser/CORPUS_TRAINTXT'

# Créer le dossier de sortie s'il n'existe pas
os.makedirs(dossier_sortie, exist_ok=True)

# Extraction et conversion
for fichier_pdf in os.listdir(dossier_pdf):
    if fichier_pdf.endswith('.pdf'):
        parseur(os.path.join(dossier_pdf, fichier_pdf), dossier_sortie)
