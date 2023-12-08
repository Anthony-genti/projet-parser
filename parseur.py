import subprocess
import os
import re
import xml.etree.ElementTree as ET
import argparse

#Conversion en utilisant pdftotext vers un fichier txt
def conversion(nom_pdf):
    fichier_pdf = nom_pdf + '.pdf'
    fichier_sortie = nom_pdf + '.txt'

    cmd = f"pdftotext -layout'{fichier_pdf}' '{fichier_sortie}'"
    resultat = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if resultat.returncode == 0:
        with open(fichier_sortie, 'r') as fichier:
            texte = fichier.read()
    return -1 ;


#Recuperer le nom du fichier
def nom(filename):
    nomFichier = filename.split('.pdf')[0]
    if ' ' in nomFichier:
        nomFichier = nomFichier.replace(' ', '_')

    # Obtenir l'extension du fichier d'entrée
    fichier_parts = nomFichier.rsplit('.', 1)
    if len(fichier_parts) > 1:  # Vérifier s'il y a une extension
        nom_fichier, extension = fichier_parts
        fichier_copie = nom_fichier + '_copie.' + extension
    else:
        nom_fichier = fichier_parts[0]
        extension = 'txt'  # Extension par défaut si aucune n'est présente
        fichier_copie = nom_fichier + '_copie.' + extension

    with open(fichier_copie, 'w', encoding='utf-8') as copie:
        copie.write(f"<nom>{nom_fichier}</nom>")

   
#Recuperer le titre du papier 
def titre(fichierTexte):
    # Obtenir l'extension du fichier d'entrée
    nom_fichier, extension = fichierTexte.rsplit('.', 1)
    
    # Créer une copie distincte du fichier original avec la même extension
    fichier_copie = nom_fichier + '_copie.' + extension
    
    majuscule1 = False
    majuscule2 = False
    
    # Premier cas : si les deux premières lignes sont en majuscules
    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()
        with open(fichier_copie, 'a', encoding='utf-8') as copie: 
            copie.write("\n")
            copie.write("<titre>")          
            if lignes[0].strip().isupper() and lignes[1].strip().isupper():
                majuscule1 = True 
                majuscule2 = True
                copie.write(lignes[0])
                copie.write(lignes[1])
                           
            if majuscule1 and majuscule2:
                copie.write("</titre>") 
                copie.write(" ")
                return "Conversion titre terminée : les deux premieres ligne sont en majuscules"
            
    # Deuxième cas : la deuxième ligne commence par une minuscule donc le titre est sur deux lignes. Aussi cas du 'for' a la fin de la première ligne
    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()
        with open(fichier_copie, 'a', encoding='utf-8') as copie:
            if len(lignes) > 1 and len(lignes[1].strip()) > 0 and lignes[1].strip()[0].islower():
                copie.write(lignes[0])
                copie.write(lignes[1])
                copie.write("</titre>")
                copie.write(" ")
                return "Conversion titre terminée : première ligne majuscule, deuxième ligne minuscule"
            
            if len(lignes) > 1 and len(lignes[1].strip()) > 0 and lignes[1].strip()[0].isupper():
                copie.write(lignes[0])  
                if lignes[0].strip().endswith("for"):
                    copie.write(lignes[1])
                    copie.write("</titre>")
                    copie.write(" ")
                    return "Conversion titre terminée : les deux lignes sont à prendre car la deuxième se termine par 'for'"
                copie.write("</titre>")
                copie.write(" ")
                return "Conversion titre terminée : seule la première ligne à prendre"

    
    #Troisieme cas : le texte commence par From: alors o recupere la premiere migne non vide pour le titre
    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()
        with open(fichier_copie, 'a', encoding='utf-8') as copie:
            index = 0
            if lignes[index].strip().startswith("From:"):
                index += 1
                while index < len(lignes) and not lignes[index].strip():
                    index += 1

                if index < len(lignes):
                    copie.write(lignes[index])
                    copie.write("</titre>")
                    copie.write(" ")
                    return "Conversion titre terminée : première ligne commence par 'From:', texte copié après"

    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()
        with open(fichier_copie, 'a', encoding='utf-8') as copie:
            index = 0
            while index < len(lignes) and not lignes[index].strip().startswith("Journal"):
                index += 1

            if index < len(lignes) and lignes[index].strip().startswith("Journal"):
                index += 1
                while index < len(lignes) and (not lignes[index].strip() or lignes[index].strip().startswith("Submitted")):
                    index += 1

                copie.write(lignes[index])
                copie.write(lignes[index+1])
                
            copie.write("</titre>")
            copie.write(" ")
            return "Conversion titre terminée : texte après 'Journal' copié hormis Submitted"


#Recuperer l'introduction 
def introduction(fichierTexte):
    # Obtenir l'extension du fichier d'entrée
    nom_fichier, extension = fichierTexte.rsplit('.', 1)
    
    # Créer une copie distincte du fichier original avec la même extension
    fichier_copie = nom_fichier + '_copie.' + extension

    previous_line = '' 

    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()        
        with open(fichier_copie, 'a', encoding='utf-8') as copie:
            introduction_started = False
            copie.write("\n")
            copie.write("<introduction>")
            for line in lignes:
                if line.startswith("Introduction") or line.startswith("I.") or line.startswith("1 Introduction") or line.startswith("1. Introduction") or line.startswith("INTRODUCTION") :
                    introduction_started = True              

                if introduction_started and "deterministic model" in line:
                    copie.write(line)
                    copie.write("</introduction>")
                    copie.write(" ")
                    return "Ajout introduction jusqu'à la combinaison 'deterministic model'"
                
                if introduction_started and line.startswith("Method") :
                    copie.write("</introduction>")
                    copie.write(" ")
                    return "Ajout introduction jusqu'à la combinaison Method"

                if introduction_started and line.startswith("II.") :
                    copie.write("</introduction>")
                    copie.write(" ")
                    return "Ajout introduction jusqu'au symbole II."

                if introduction_started and line.startswith("2.") :
                    copie.write("</introduction>")
                    copie.write(" ")
                    return "Ajout introduction jusqu'au symbole 2."

                if introduction_started and line.startswith("2") :
                    copie.write("</introduction>")
                    copie.write(" ")
                    return "Ajout introduction jusqu'au symbole 2 avec ligne avant vide"
                    
                if introduction_started :
                    copie.write(line)

                previous_line = line


def corps(fichierTexte):
    # Obtenir l'extension du fichier d'entrée
    nom_fichier, extension = fichierTexte.rsplit('.', 1)
    
    # Créer une copie distincte du fichier original avec la même extension
    fichier_copie = nom_fichier + '_copie.' + extension

    previous_line = '' 

    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()        
        with open(fichier_copie, 'a', encoding='utf-8') as copie:
            introduction_started = False
            corps_started = False
            copie.write("\n")
            copie.write("<corps>")
            for line in lignes:
                if corps_started and "CONCLUSIONS" in line or "Conclusion" in line or line.startswith("Conclusions") or "Discussion" in line :
                    copie.write("</corps>")
                    copie.write(" ")
                    return "Corps extrait" 
                          
                if line.startswith("Introduction") or line.startswith("I.") or line.startswith("1 Introduction") or line.startswith("1. Introduction") or line.startswith("INTRODUCTION") :
                    introduction_started = True              

                if introduction_started and "deterministic model" in line:        
                    corps_started = True
                
                if introduction_started and line.startswith("Method") :
                   corps_started = True

                if introduction_started and line.startswith("II.") :
                    corps_started = True

                if introduction_started and line.startswith("2.") :
                    corps_started = True

                if introduction_started and line.startswith("2") :
                    corps_started = True
                    
                if corps_started :
                    copie.write(line)
                    
               
def acknowledgement(fichierTexte):
    # Obtenir l'extension du fichier d'entrée
    nom_fichier, extension = fichierTexte.rsplit('.', 1)
    
    # Créer une copie distincte du fichier original avec la même extension
    fichier_copie = nom_fichier + '_copie.' + extension

    previous_line = '' 

    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()        
        with open(fichier_copie, 'a', encoding='utf-8') as copie:
            acknowledgement_started = False
            corps_started = False
            copie.write("\n")
            copie.write("<acknowledgement>")
            for line in lignes :
                if line.startswith("Acknowledgements") :
                    acknowledgement_started=True              
                if line.startswith("References"):
                    copie.write("</acknowledgement>")
                    copie.write(" ")
                    return 
                if acknowledgement_started :
                    copie.write(line)
            


def abstract(fichierTexte):
    # Obtenir l'extension du fichier d'entrée
    nom_fichier, extension = fichierTexte.rsplit('.', 1)   
    # Créer une copie distincte du fichier original avec la même extension
    fichier_copie = nom_fichier + '_copie.' + extension

    previous_line = '' 

    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()   
        abstract_started = False
        with open(fichier_copie, 'a', encoding='utf-8') as copie:
            copie.write("\n")
            copie.write("<abstract>")            
            for line in lignes:
                if line.startswith("Abstract") or line.startswith("Abstract-") or line.startswith("In this article") or line.startswith("ABSTRACT") :
                    abstract_started = True 
                
                if abstract_started and line.startswith("1") and previous_line.strip() == '' :
                    copie.write("</abstract>")
                    return "Abstract extrait arret car lecture 1" 
                                  
                if abstract_started and line.startswith("1 Introduction") :
                    copie.write("</abstract>")
                    return "Abstract extrait arret car  1 Introduction" 
                
                if abstract_started and line.startswith("I.") :
                    copie.write("</abstract>")
                    return "Abstract extrait arret car lecture I." 
                
                if abstract_started and line.startswith("Introduction") :
                    copie.write("</abstract>")
                    return "Abstract extrait arret car lecture Introduction" 
                
                if abstract_started and line.startswith("1. Introduction") :
                    copie.write("</abstract>")
                    return "Abstract extrait arret car lecture 1. Introduction" 
                
                if abstract_started :
                    copie.write(line)
                                      
                previous_line = line 
   

#Recuperer auteur
def auteur(fichierTexte):
    # Obtenir l'extension du fichier d'entrée
    nom_fichier, extension = fichierTexte.rsplit('.', 1)

    # Créer une copie distincte du fichier original avec la même extension
    fichier_copie = nom_fichier + '_copie.' + extension

    ligneTitre = ''

    with open(fichier_copie, 'r') as file:
        texte = file.read()
        resultat = re.search(r'<titre>(.*?)</titre>', texte, re.DOTALL)
        if resultat:
            ligneTitre = resultat.group(1).strip().split('\n')
            if len(ligneTitre) >= 2:
                x1 = ligneTitre[0][:10]
                x2 = ligneTitre[1][:10]
            else:
                x1 = ligneTitre[0][:10]
                x2 = x1

    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()
        with open(fichier_copie, 'a', encoding='utf-8') as copie:
            copie.write("\n")
            copie.write("<auteur>")
            for line in lignes:
                try:
                    if (line.startswith("Abstract") or line.startswith("Abstract-") or
                            line.startswith("In this article") or line.startswith("ABSTRACT")):
                        copie.write("</auteur>")
                        return
                    if not x1 in line:
                        if not x2 in line:
                            copie.write(line)
                except UnicodeDecodeError:
                    # En cas d'erreur, ne rien faire
                    pass
                        
                               
def conclusion(fichierTexte):
    # Obtenir l'extension du fichier d'entrée
    nom_fichier, extension = fichierTexte.rsplit('.', 1)
    
    # Créer une copie distincte du fichier original avec la même extension
    fichier_copie = nom_fichier + '_copie.' + extension

    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()        
        with open(fichier_copie, 'a', encoding='utf-8') as copie:
            conclusion_started = False
            copie.write("\n")
            copie.write("<conclusion>")
            for line in lignes:
                if "VI. C ONCLUSIONS" in line or "Conclusion" in line or "CONCLUSIONS" in line or "Conclusions" in line :
                    conclusion_started = True              

                if conclusion_started and "Acknowledgements" in line or "References" in line or "ACKNOWLEDGMENT" in line or "Acknowledgments" in line:
                    copie.write("</conclusion>")
                    return 

                if conclusion_started :
                    copie.write(line)
                


def references(fichierTexte):
    # Obtenir l'extension du fichier d'entrée
    nom_fichier, extension = fichierTexte.rsplit('.', 1)
    
    # Créer une copie distincte du fichier original avec la même extension
    fichier_copie = nom_fichier + '_copie.' + extension

    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()        
        with open(fichier_copie, 'a', encoding='utf-8') as copie:
            references_started = False
            copie.write("\n")
            copie.write("<references>")
            for line in lignes:
                if "References" in line or "Références" in line or "R EFERENCES" in line or line.startswith("REFERENCES") :
                    references_started = True              
                if references_started :
                    copie.write(line)
            copie.write("</references>")    
     

   
def discussion(fichierTexte):
    # Obtenir l'extension du fichier d'entrée
    nom_fichier, extension = fichierTexte.rsplit('.', 1)
    
    # Créer une copie distincte du fichier original avec la même extension
    fichier_copie = nom_fichier + '_copie.' + extension

    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()        
        with open(fichier_copie, 'a', encoding='utf-8') as copie:
            discussion_started = False
            copie.write("\n")
            copie.write("<discussion>")
            for line in lignes:
                if "Discussion" in line or "DISCUSSION" in line :
                    discussion_started=True
                
                if discussion_started and "Acknowledgments" in line or "Conclusions" in line or "7. CONCLUSIONS" in line :
                    copie.write("</discussion>")
                    return 
          
                if discussion_started:
                    copie.write(line)

      


def gestionCasExceptionnel(fichierTexte, chaineDebut, chaineFin, chaineApresLaquelleInserer):
    with open(fichierTexte, 'r', encoding='utf-8') as file:
        lignes = file.readlines()
        debut = False
        fin = False
        extrait = []

        for line in lignes:
            if chaineDebut in line:
                debut = True

            if debut and not fin:
                extrait.append(line)

            if chaineFin in line:
                fin = True

        file.seek(0)  # Retour au début du fichier
        with open(fichierTexte, 'w', encoding='utf-8') as output_file:
            for line in lignes:
                if chaineApresLaquelleInserer in line:
                    output_file.writelines(extrait)
                output_file.write(line)




def convert_txt_to_xml(input_file):
    # Vérifier si le fichier texte existe
    if not os.path.isfile(input_file):
        return "Le fichier texte spécifié n'existe pas."

    output_file = os.path.splitext(input_file)[0] + ".xml"  # Nom du fichier XML de sortie

    # Créer l'élément racine du XML
    root = ET.Element("Root")

    # Lire le contenu du fichier texte
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Convertir chaque ligne du fichier texte en éléments XML
    for line in lines:
        key, value = line.strip().split(': ')
        element = ET.SubElement(root, key)
        element.text = value

    # Créer l'arbre XML
    tree = ET.ElementTree(root)

    # Enregistrer l'arbre XML dans un fichier
    tree.write(output_file)

    return f"Le fichier XML '{output_file}' a été créé avec succès."



def parseur(listeFichierPDF, mode):
    fichiers_a_parser = []

    for i, x in enumerate(listeFichierPDF, 1):
        nom_pdf = os.path.splitext(x)[0]  # Obtenir le nom original sans extension
        print(f"{i}. Nom du fichier PDF sans extension : {nom_pdf}")

    if mode == 't':
        choix = input("Entrez les numéros des fichiers PDF à parser (séparés par des espaces) : ")
        nums = [int(num.strip()) for num in choix.split()]

        for num in nums:
            pdf = listeFichierPDF[num - 1]
            txt_output = conversion(pdf)
            fichiers_a_parser.append(f"{os.path.splitext(pdf)[0]}.txt")

        for t in fichiers_a_parser:
            titre(t)
            auteur(t)
            abstract(t)
            introduction(t)
            corps(t)
            conclusion(t)
            acknowledgement(t)
            references(t)
            discussion(t)   

    elif mode == 'x':
        choix = input("Entrez les numéros des fichiers PDF à parser (séparés par des espaces) : ")
        nums = [int(num.strip()) for num in choix.split()]
        fichier_a_convertir_en_xml = []

        for num in nums:
            pdf = listeFichierPDF[num - 1]
            txt_output = conversion(pdf)
            fichiers_a_parser.append(f"{os.path.splitext(pdf)[0]}.txt")

        for t in fichiers_a_parser:
            titre(t)
            auteur(t)
            abstract(t)
            introduction(t)
            corps(t)
            conclusion(t)
            acknowledgement(t)
            references(t)
            discussion(t)   
            fichier_a_convertir_en_xml.append(t.replace(".txt", "_copie.txt"))
        
        #for y in fichier_a_convertir_en_xml:
            #convert_txt_to_xml(y)
                      

    return "Parsement effectué" 

#Gestion -t -x 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parseur de fichiers PDF')
    parser.add_argument('-t', action='store_true', help='Option pour traitement normal (-t)')
    parser.add_argument('-x', action='store_true', help='Option pour traitement spécial (-x)')

    args = parser.parse_args()

    fichiers_pdf = [fichier for fichier in os.listdir() if fichier.endswith('.pdf')]

    if args.t:
        parseur(fichiers_pdf, 't')
    elif args.x:
        parseur(fichiers_pdf, 'x')
    else:
        print("Veuillez spécifier une option -t ou -x.")


        

