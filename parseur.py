import sys
import os
import subprocess
import re

def parseur(fichier_pdf, dossier_sortie, sortie_texte=False, sortie_xml=False):
    if os.path.exists(fichier_pdf):
        nom_fichier = os.path.splitext(os.path.basename(fichier_pdf))[0]
        fichier_sortie = os.path.join(dossier_sortie, f"{nom_fichier}")

        cmd = f"pdftotext '{fichier_pdf}' '{fichier_sortie}.txt'"
        resultat = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if resultat.returncode == 0:
            with open(f"{fichier_sortie}.txt", 'r') as fichier:
                texte = fichier.read()

            correspondance_auteurs = re.search(r'Auteurs\n(.*?)Abstract\n', texte, re.DOTALL)
            auteurs = correspondance_auteurs.group(1).replace('\n', ' ').strip() if correspondance_auteurs else ""

            correspondance_titre = re.search(r'Titre\n(.*?)Abstract\n', texte, re.DOTALL)
            titre = correspondance_titre.group(1).replace('\n', ' ').strip() if correspondance_titre else ""

            correspondance_abstract = re.search(r'Abstract\n(.*?)(?:\s1\s|\sI\s|\sIntroduction\s|$)', texte, re.DOTALL)
            abstract = correspondance_abstract.group(1).replace('\n', ' ').strip() if correspondance_abstract else ""

            correspondance_introduction = re.search(r'Introduction\n(.*?)(?=\n\d+\.|\Z)', texte, re.DOTALL)
            introduction = correspondance_introduction.group(1).replace('\n', ' ').strip() if correspondance_introduction else ""

            correspondance_corps = re.search(r'Développement\n(.*?)(?=\n(?:\d+\.|Conclusion\b|Discussion\b))', texte, re.DOTALL)
            corps = correspondance_corps.group(1).replace('\n', ' ').strip() if correspondance_corps else ""

            correspondance_conclusion = re.search(r'Conclusion\n(.*?)(?=\n(?:\d+\.|Discussion\b))', texte, re.DOTALL)
            conclusion = correspondance_conclusion.group(1).replace('\n', ' ').strip() if correspondance_conclusion else ""

            correspondance_discussion = re.search(r'Discussion\n(.*?)(?=\n(?:\d+\.|Références\b))', texte, re.DOTALL)
            discussion = correspondance_discussion.group(1).replace('\n', ' ').strip() if correspondance_discussion else ""

            correspondance_references = re.search(r'Références\n(.*?)(?=\n\w|\Z)', texte, re.DOTALL)
            references = correspondance_references.group(1).strip() if correspondance_references else ""

            informations_formatees = f"Nom du fichier d'origine : {nom_fichier}\n"
            informations_formatees += f"Auteurs et leurs adresses : {auteurs}\n"
            informations_formatees += f"Titre du papier : {titre}\n"
            informations_formatees += f"Résumé de l'article : {abstract}\n"
            informations_formatees += f"Introduction : {introduction}\n"
            informations_formatees += f"Développement : {corps}\n"
            informations_formatees += f"Conclusion : {conclusion}\n"
            informations_formatees += f"Discussion : {discussion}\n"
            informations_formatees += f"Références bibliographiques :\n{references}\n"

            if sortie_texte:
                with open(f"{fichier_sortie}.txt", 'w') as fichier_texte:
                    fichier_texte.write(informations_formatees)
            elif sortie_xml:
                xml_content = f'<article>\n' \
                               f'   	<preamble>Le nom du fichier d’origine : {nom_fichier}</preamble>\n' \
                               f'   	<titre>Le titre du papier : {titre}</titre>\n' \
                               f'   	<auteur>Auteurs et leurs adresses : {auteurs}</auteur>\n' \
                               f'   	<abstract>Résumé de l’article : {abstract}</abstract>\n' \
                               f'   	<introduction>Introduction : {introduction}</introduction>\n' \
                               f'   	<corps>Développement : {corps}</corps>\n' \
                               f'   	<conclusion>Conclusion : {conclusion}</conclusion>\n' \
                               f'   	<discussion>Discussion : {discussion}</discussion>\n' \
                               f'   	<biblio>Références bibliographiques :\n{references}</biblio>\n' \
                               f'</article>'

                with open(f"{fichier_sortie}.xml", 'w', encoding='utf-8') as fichier_xml:
                    fichier_xml.write(xml_content)

                if os.path.exists(f"{fichier_sortie}.txt"):
                    os.remove(f"{fichier_sortie}.txt")

        else:
            print(f"Erreur lors de l'extraction du texte : {resultat.stderr.decode('utf-8').strip()}")
    else:
        print(f"Le fichier PDF '{fichier_pdf}' n'existe pas.")

# Gérer les arguments de la ligne de commande manuellement
if len(sys.argv) < 4:
    print("Usage: python parseur.py dossier_entree dossier_sortie [-t | -x]")
    sys.exit(1)

dossier_entree = sys.argv[1]
dossier_sortie = sys.argv[2]
sortie_texte = '-t' in sys.argv
sortie_xml = '-x' in sys.argv

if not sortie_texte and not sortie_xml:
    print("Veuillez spécifier l'option -t (texte) ou -x (XML).")
    sys.exit(1)

# Afficher tous les fichiers PDF disponibles dans le dossier d'entrée avec leurs numéros
print("Fichiers PDF disponibles dans le dossier spécifié :")
fichiers_pdf = [fichier for fichier in os.listdir(dossier_entree) if fichier.endswith('.pdf')]
for i, fichier in enumerate(fichiers_pdf, 1):
    print(f"{i}. {fichier}")

# Demander à l'utilisateur de choisir les fichiers à convertir
choix_utilisateur = input("Entrez les numéros des fichiers à convertir (séparés par des virgules) : ")
numeros_selectionnes = [int(num.strip()) for num in choix_utilisateur.split(',') if num.strip().isdigit()]
fichiers_a_convertir = [fichiers_pdf[num - 1] for num in numeros_selectionnes if 0 < num <= len(fichiers_pdf)]

if not fichiers_a_convertir:
    print("Aucun fichier sélectionné pour la conversion.")
    sys.exit()

# Convertir les fichiers sélectionnés
for fichier_pdf in fichiers_a_convertir:
    chemin_pdf = os.path.join(dossier_entree, fichier_pdf)
    parseur(chemin_pdf, dossier_sortie, sortie_texte, sortie_xml)
