import subprocess
import os

#Conversion en utilisant pdftotext vers un fichier txt
def conversion(nom_pdf):
    fichier_pdf = nom_pdf + '.pdf'
    fichier_sortie = nom_pdf + '.txt'

    cmd = f"pdftotext '{fichier_pdf}' '{fichier_sortie}'"
    resultat = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if resultat.returncode == 0:
        with open(fichier_sortie, 'r') as fichier:
            texte = fichier.read()
    return -1 ;


#Injecter le nom dans le fichier texte de sortie : OK 
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
            copie.write("<titre>")          
            if len(lignes) > 0 and lignes[0].strip().isupper():
                majuscule1 = True 
            
            if len(lignes) > 1 and lignes[1].strip().isupper():
                copie.write(lignes[1])
                majuscule2 = True 
            
            if majuscule1 and majuscule2:
                copie.write("</titre>")
                return "Conversion titre terminée : les deux premieres ligne sont en majuscules"
            
    # Deuxième cas : la deuxième ligne commence par une minuscule donc le titre est sur deux lignes. Aussi cas du 'for' a la fin de la première ligne
    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()
        with open(fichier_copie, 'a', encoding='utf-8') as copie:
            if len(lignes) > 1 and len(lignes[1].strip()) > 0 and lignes[1].strip()[0].islower():
                copie.write(lignes[0])
                copie.write(lignes[1])
                copie.write("</titre>")
                return "Conversion titre terminée : première ligne majuscule, deuxième ligne minuscule"
            
            if len(lignes) > 1 and len(lignes[1].strip()) > 0 and lignes[1].strip()[0].isupper():
                copie.write(lignes[0])  
                if lignes[0].strip().endswith("for"):
                    copie.write(lignes[1])
                    copie.write("</titre>")
                    return "Conversion titre terminée : les deux lignes sont à prendre car la deuxième se termine par 'for'"
                copie.write("</titre>")
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
            return "Conversion titre terminée : texte après 'Journal' copié hormis Submitted"


def introduction(fichier):
    # Obtenir l'extension du fichier d'entrée
    nom_fichier, extension = fichierTexte.rsplit('.', 1)
    
    # Créer une copie distincte du fichier original avec la même extension
    fichier_copie = nom_fichier + '_copie.' + extension

    previous_line = '' 

    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()        
        with open(fichier_copie, 'w', encoding='utf-8') as copie:
            introduction_started = False
            for line in lignes:
                if line.startswith("Introduction") or line.startswith("I.") or line.startswith("1 Introduction") or line.startswith("1. Introduction") or line.startswith("INTRODUCTION") :
                    introduction_started = True              

                if introduction_started and "deterministic model" in line:
                    copie.write(line)
                    return "Ajout introduction jusqu'à la combinaison 'deterministic model'"
                
                if introduction_started and line.startswith("Method") :
                    return "Ajout introduction jusqu'à la combinaison Method"

                if introduction_started and line.startswith("II.") :
                    return "Ajout introduction jusqu'au symbole II."

                if introduction_started and line.startswith("2.") :
                    return "Ajout introduction jusqu'au symbole 2."

                if introduction_started and line.startswith("2") :
                    return "Ajout introduction jusqu'au symbole 2 avec ligne avant vide"
                    
                if introduction_started :
                    copie.write(line)

                previous_line = line


def abstract(fichierTexte):
    # Obtenir l'extension du fichier d'entrée
    nom_fichier, extension = fichierTexte.rsplit('.', 1)
    
    # Créer une copie distincte du fichier original avec la même extension
    fichier_copie = nom_fichier + '_copie.' + extension

    previous_line = '' 

    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()        
        with open(fichier_copie, 'w', encoding='utf-8') as copie:
            abstract_started = False
            for line in lignes:
                if line.startswith("Abstract") or line.startswith("Abstract-") or line.startswith("In this article") or line.startswith("ABSTRACT") :
                    abstract_started = True 
                
                if abstract_started and line.startswith("1") and previous_line.strip() == '' :
                    return "Abstract extrait arret car lecture 1" 
                                  
                if abstract_started and line.startswith("1 Introduction") :
                    return "Abstract extrait arret car  1 Introduction" 
                
                if abstract_started and line.startswith("I.") :
                    return "Abstract extrait arret car lecture I." 
                
                if abstract_started and line.startswith("Introduction") :
                    return "Abstract extrait arret car lecture Introduction" 
                
                if abstract_started and line.startswith("1. Introduction") :
                    return "Abstract extrait arret car lecture 1. Introduction" 
                
                if abstract_started :
                    copie.write(line)
                                      
                previous_line = line 
   

##recuperer ce qu'il y'a entre la fin du titre et l'abstract
def auteur(fichierTexte):
    return 0 ;


pdf_nom = ['Torres','ACL2004-HEADLINE','Boudin-Torres-2006','compression','compression_phrases_Prog-Linear-jair','hybrid_approach','marcu_statistics_sentence_pass_one','mikheev','probabilistic_sentence_reduction','Stolcke_1996_Automatic_linguistic']
txt_nom = ['Torres.txt','ACL2004-HEADLINE.txt','Boudin-Torres-2006.txt','compression.txt','compression_phrases_Prog-Linear-jair.txt','hybrid_approach.txt','marcu_statistics_sentence_pass_one.txt','mikheev.txt','probabilistic_sentence_reduction.txt','Stolcke_1996_Automatic_linguistic.txt']


#Afficher le nom et append dans le fichier copie
for x in pdf_nom :
   print(f"Nom du fichier PDF sans extension : {nom(x)}")
   print(" ")
   
#Faire la conversion pdf vers txt   
for y in pdf_nom:
    txt_output = conversion(y)
    print(f"Fichier texte converti : {y}")
    print(" ")

#Test extraction titre 
for t in txt_nom :
   titre(t)
   print(" ")

#Test extraction introduction
#for t in txt_nom:
    #print(t)
    #print(introduction(t))
    #print("********************************************************************")
    
    
#Test extraction abstract
#for t in txt_nom:
    #print(t)
    #print(abstract(t))
    #print("-----------------------------------------------------------------------")


#Test extraction auteur

#Test extraction introduction

