# projet-parser

@README.md

Programme de Conversion de PDF en Texte ou en XML.

Ce programme Python vous permet de transformer des fichiers PDF en fichiers texte ou en xml selon loption donnée en argument soit version texte (-t) soit au format XML (-x) .Tout en récupérant des données spécifiques comme le titre du document et le résumé de l'auteur. Les informations extraites seront organisées et sauvegardées dans un fichier texte de sortie ou dans un fichier xml de sortie de la forme:
<article>
  <preamble> Le nom du fichier d’origine </preamble>
  <titre> Le titre du papier </titre>
  <auteur> La section auteurs et leur adresse </auteur>
  <abstract> Le résumé de l’article </abstract>
  <biblio> Les références bibliographiques du papier</biblio>
</article>

 Voici comment utiliser ce programme.

Prérequis

Avant tout, assurez-vous d'avoir Python (notamment Python3) installé sur votre ordinateur. Vous devrez également disposer de l'outil de conversion PDF en texte pdftotext du package poppler-utils. Pour l'obtenir, exécutez dans un terminal : 

sudo apt-get install poppler-utils

Pour l'installation de notre outil vérifiez si la bibliothèque Python PyPDF2 est installée. Si elle ne l'est pas, vous pouvez l'installer avec la commande suivante :

pip install PyPDF2

Pour l'utilisation :

1. Placez vos fichiers PDF dans un dossier de votre choix.
2. Exécutez le programme en utilisant cette commande :

python parseur.py /chemin/vers/votre/fichier_pdf /chemin/vers/dossier_de_sortie -t | -x .
/chemin/vers/votre/fichier_pdf : Remplacez ceci par le chemin absolu du dossier contenant vos fichiers PDF.
/chemin/vers/dossier_de_sortie : Remplacez ceci par le chemin absolu du dossier où vous souhaitez enregistrer les fichiers texte convertis avec les informations extraites.
version texte (-t) ou version XML (-x).
