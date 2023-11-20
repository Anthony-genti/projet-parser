import os
import xml.etree.ElementTree as ET

def extraire_informations(fichier_xml, fichier_sortie):
    try:
        tree = ET.parse(fichier_xml)
        root = tree.getroot()

        informations = []

        for element in root.iter():
            if element.text and ":" in element.text:
                cle, valeur = element.text.split(":", 1)
                informations.append(f"{cle.strip()} : {valeur.strip()}")

        with open(fichier_sortie, 'a', encoding='utf-8') as fichier_texte:
            fichier_texte.write("\n".join(informations))
            fichier_texte.write("\n\n")

    except Exception as e:
        print(f"Erreur lors de l'extraction des informations du fichier {fichier_xml}: {str(e)}")

def parcourir_dossier_xml(dossier_entree, fichier_sortie):
    fichiers_xml = [fichier for fichier in os.listdir(dossier_entree) if fichier.endswith('.xml')]

    for fichier_xml in fichiers_xml:
        chemin_xml = os.path.join(dossier_entree, fichier_xml)
        extraire_informations(chemin_xml, fichier_sortie)

# Spécifiez le dossier d'entrée et le fichier de sortie
dossier_entree = '/mnt/c/Users/antho/Desktop/usb/L3/genie logiciel/CORPUS_TRAIN/transforme_xml'
fichier_sortie = '/mnt/c/Users/antho/Desktop/usb/L3/genie logiciel/CORPUS_TRAIN/resultat.txt'

# Appel de la fonction pour parcourir le dossier XML
parcourir_dossier_xml(dossier_entree, fichier_sortie)
