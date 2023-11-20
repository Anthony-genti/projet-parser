@README.md

Programme de Conversion de PDF en Texte

Ce programme Python vous permet de transformer des fichiers PDF en fichiers texte tout en récupérant des données spécifiques comme le titre du document et le résumé de l'auteur. Les informations extraites seront organisées et sauvegardées dans un fichier texte de sortie. Voici comment utiliser ce programme.

Prérequis

Avant tout, assurez-vous d'avoir Python (notamment Python3) installé sur votre ordinateur. Vous devrez également disposer de l'outil de conversion PDF en texte pdftotext du package poppler-utils. Pour l'obtenir, exécutez dans un terminal : 

sudo apt-get install poppler-utils

Pour l'installation de notre outil vérifiez si la bibliothèque Python PyPDF2 est installée. Si elle ne l'est pas, vous pouvez l'installer avec la commande suivante :

pip install PyPDF2

Pour l'utilisation :

1. Placez vos fichiers PDF dans un dossier de votre choix.
2. Exécutez le programme en utilisant cette commande :

python convert_pdf_to_text.py /chemin/vers/votre/dossier_pdf /chemin/vers/dossier_de_sortie
/chemin/vers/votre/dossier_pdf : Remplacez ceci par le chemin absolu du dossier contenant vos fichiers PDF.
/chemin/vers/dossier_de_sortie : Remplacez ceci par le chemin absolu du dossier où vous souhaitez enregistrer les fichiers texte convertis avec les informations extraites.

Le programme fera automatiquement ce qui suit :
1. Parcourir les fichiers PDF dans le dossier spécifié.
2. Extraire les informations nécessaires.
3. Remplacer les espaces dans le titre par des underscores (_).
4. S'assurer que le résumé est sur une seule ligne dans le fichier de sortie.

Les fichiers texte résultants contiendront les informations extraites et seront sauvegardés dans le dossier de sortie spécifié.
