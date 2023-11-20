import sys
import os
import subprocess
import re

def parseur(fichier_pdf, dossier_sortie, sortie_texte=False, sortie_xml=False):
    if os.path.exists(fichier_pdf):
        nom_fichier = os.path.splitext(os.path.basename(fichier_pdf))[0]
        fichier_sortie = os.path.join(dossier_sortie, f"{nom_fichier}")

        # Utilisation de pdftotext pour extraire le texte du PDF
        cmd = f"pdftotext '{fichier_pdf}' '{fichier_sortie}.txt'"
        resultat = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if resultat.returncode == 0:
            with open(f"{fichier_sortie}.txt", 'r') as fichier:
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

            if sortie_texte:
                # Informations dans le fichier de sortie texte
                with open(f"{fichier_sortie}.txt", 'w') as fichier_texte:
                    fichier_texte.write(informations_formatees)
            elif sortie_xml:
                # Informations dans le fichier de sortie XML
                xml_content = f'<article>\n' \
                              f'       <preamble>Le nom du fichier d’origine : {nom_fichier}</preamble>\n' \
                              f'       <titre>Le titre du papier : {titre}</titre>\n' \
                              f'       <auteur>La section auteurs et leur adresse : </auteur>\n' \
                              f'       <abstract>Le résumé de l’article : {abstract}</abstract>\n' \
                              f'       <biblio>Les références bibliographiques du papier</biblio>\n' \
                              f'</article>'

                with open(f"{fichier_sortie}.xml", 'w', encoding='utf-8') as fichier_xml:
                    fichier_xml.write(xml_content)

            # Si l'option XML est spécifiée et pas l'option texte, ne pas écrire le fichier texte
            if sortie_xml and not sortie_texte:
                os.remove(f"{fichier_sortie}.txt")

        else:
            print(f"Erreur lors de l'extraction du texte : {resultat.stderr.decode('utf-8').strip()}")
    else:
        print(f"Le fichier PDF '{fichier_pdf}' n'existe pas.")

# Gérer les arguments de la ligne de commande manuellement
if len(sys.argv) < 4:
    print("Usage: python parseur.py fichier_pdf dossier_sortie [-t | -x]")
    sys.exit(1)

fichier_pdf = sys.argv[1]
dossier_sortie = sys.argv[2]
sortie_texte = '-t' in sys.argv
sortie_xml = '-x' in sys.argv

# Assurer que l'utilisateur a sélectionné une option valide
if not sortie_texte and not sortie_xml:
    print("Veuillez spécifier l'option -t (texte) ou -x (XML).")
    sys.exit(1)

# Créer le dossier de sortie s'il n'existe pas
os.makedirs(dossier_sortie, exist_ok=True)

# Exécuter la conversion en texte ou en XML en fonction de l'option spécifiée
parseur(fichier_pdf, dossier_sortie, sortie_texte, sortie_xml)
