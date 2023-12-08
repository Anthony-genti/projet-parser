import subprocess
import os
import re
import argparse
from pathlib import Path

#Conversion en utilisant pdftotext vers un fichier txt
def conversion(nom_pdf):
    fichier_pdf = nom_pdf 
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

    ligneTitre=''  
   
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
            for line in lignes :
                if (line.startswith("Abstract") or line.startswith("Abstract-") or line.startswith("In this article") or line.startswith("ABSTRACT")) :
                    copie.write("</auteur>")
                    return   
                                   
                if not x1 in line :
                    if not x2 in line :
                        copie.write(line)
                        
                               
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

           

def parseur(listePDF) :
    #Doit contenir les pdf
    fichiers_a_parser = []

    for i, x in enumerate(listePDF, 1):
        nom_pdf = os.path.splitext(x)[0]  # Obtenir le nom original sans extension
        print(f"{i}. Nom du fichier PDF sans extension : {nom_pdf}")

    choix = input("Entrez les numéros des fichiers PDF à parser (séparés par des espaces) : ")
    nums = [int(num.strip()) for num in choix.split()]

    for num in nums:
        pdf = listePDF[num - 1]
        fichiers_a_parser.append(f"{pdf}")
        
    #A ce moment la il y'a tout les pdf a parser dans fichiers_a_parser

    for x in fichiers_a_parser :
        nom(x)
      
    #Faire la conversion pdf vers txt   
    for y in fichiers_a_parser:
        conversion(y)

        
    #Liste de fichier texte
    txt_nom = [y.replace(".pdf",".txt") for y in fichiers_a_parser]
            
    #Test extraction titre 
    for t in txt_nom :
        titre(t)
        print(" ")

    #Test extraction auteur
    for t in txt_nom:
        auteur(t)
        print(" ")

    #Test extraction abstract
    for t in txt_nom:
        abstract(t)
        print("  ")

    #Test extraction introduction
    for t in txt_nom:
        introduction(t)
        print(" ")
 
    #Test extraction corps  
    for t in txt_nom:
        corps(t)
        print(" ")
 
    #Test extraction conclusion
    for t in txt_nom:
        conclusion(t)
        print(" ")
    
    #Test extraction acknowledgement
    for t in txt_nom:
        acknowledgement(t)
        print(" ")

    #Test extraction references
    for t in txt_nom:
        references(t)
        print(" ")
    
    #Test extraction discussion
    for t in txt_nom:
        discussion(t)
        print(" ")
    
    
#Recuperer uniquement les fichiers pdf    
fichiers_pdf = [fichier for fichier in os.listdir() if Path(fichier).suffix.lower() == '.pdf']  
parseur(fichiers_pdf)  
    
pdf_nom = ['Torres','ACL2004-HEADLINE','Boudin-Torres-2006','compression','compression_phrases_Prog-Linear-jair','hybrid_approach','marcu_statistics_sentence_pass_one','mikheev','probabilistic_sentence_reduction','Stolcke_1996_Automatic_linguistic']
txt_nom = ['Torres.txt','ACL2004-HEADLINE.txt','Boudin-Torres-2006.txt','compression.txt','compression_phrases_Prog-Linear-jair.txt','hybrid_approach.txt','marcu_statistics_sentence_pass_one.txt','mikheev.txt','probabilistic_sentence_reduction.txt','Stolcke_1996_Automatic_linguistic.txt']


