import subprocess
import os

#Recuperer le nom du fichier. Si espace alors conversion avec des des underscores
def nom(filename):
    nomFichier = filename.split('.pdf')[0]
    if ' ' in nomFichier:
        nouveauNomFichier = nomFichier.replace(' ', '_')
        return nouveauNomFichier
    return nomFichier

#Conversion en utilisant pdftotext vers un fichier txt
def conversion(nom_pdf):
    fichier_pdf = nom_pdf + '.pdf'
    fichier_sortie = nom_pdf + '.txt'

    cmd = f"pdftotext '{fichier_pdf}' '{fichier_sortie}'"
    resultat = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if resultat.returncode == 0:
        with open(fichier_sortie, 'r') as fichier:
            texte = fichier.read()
            return texte
    return -1 ;

#Recuperer le nom du fichier. Si espace alors conversion avec des underscores
def nom(filename):
    nomFichier = filename.split('.pdf')[0]
    if ' ' in nomFichier:
        nouveauNomFichier = nomFichier.replace(' ', '_')
        return nouveauNomFichier
    return nomFichier

#Conversion en utilisant pdftotext vers un fichier txt
def conversion(nom_pdf):
    fichier_pdf = nom_pdf + '.pdf'
    fichier_sortie = nom_pdf + '.txt'

    cmd = f"pdftotext '{fichier_pdf}' '{fichier_sortie}'"
    resultat = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if resultat.returncode == 0:
        with open(fichier_sortie, 'r') as fichier:
            texte = fichier.read()
            #return texte
    return -1 ;


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
        with open(fichier_copie, 'w', encoding='utf-8') as copie:
            if len(lignes) > 0 and lignes[0].strip().isupper():
                copie.write(lignes[0])
                majuscule1 = True 
            
            if len(lignes) > 1 and lignes[1].strip().isupper():
                copie.write(lignes[1])
                majuscule2 = True 
            
            if majuscule1 and majuscule2:
                return "Conversion titre terminée"
            
    # Deuxième cas : la deuxième ligne commence par une minuscule donc le titre est sur deux lignes. Aussi cas du 'for' a la fin de la première ligne
    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()
        with open(fichier_copie, 'w', encoding='utf-8') as copie:
            if len(lignes) > 1 and len(lignes[1].strip()) > 0 and lignes[1].strip()[0].islower():
                copie.write(lignes[0])
                copie.write(lignes[1])
                return "Conversion titre terminée : première ligne majuscule, deuxième ligne minuscule"
            
            if len(lignes) > 1 and len(lignes[1].strip()) > 0 and lignes[1].strip()[0].isupper():
                copie.write(lignes[0])  
                if lignes[0].strip().endswith("for"):
                    copie.write(lignes[1])  
                    return "Conversion titre terminée : les deux lignes sont à prendre car la deuxième se termine par 'for'"
                return "Conversion titre terminée : seule la première ligne à prendre"

    
    #Troisieme cas : le texte commence par From: alors o recupere la premiere migne non vide pour le titre
    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()
        with open(fichier_copie, 'w', encoding='utf-8') as copie:
            index = 0
            if lignes[index].strip().startswith("From:"):
                index += 1
                while index < len(lignes) and not lignes[index].strip():
                    index += 1

                if index < len(lignes):
                    copie.write(lignes[index])
                    return "Conversion titre terminée : première ligne commence par 'From:', texte copié après"

    with open(fichierTexte, 'r', encoding='utf-8') as original:
        lignes = original.readlines()
        with open(fichier_copie, 'w', encoding='utf-8') as copie:
            index = 0
            while index < len(lignes) and not lignes[index].strip().startswith("Journal"):
                index += 1

            if index < len(lignes) and lignes[index].strip().startswith("Journal"):
                index += 1
                while index < len(lignes) and (not lignes[index].strip() or lignes[index].strip().startswith("Submitted")):
                    index += 1

                copie.write(lignes[index])
                copie.write(lignes[index+1])
                
                
            return "Conversion titre terminée : texte après 'Journal' copié hormis Submitted"

#a terminer
def introduction(fichierTexte):
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
                if line.startswith("Introduction") or line.startswith("I.") :
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



#Il suffit de prendre du mot Abstract jusqu'au debut de Introduction. 
#def abstract :
    #return 

#Prendre ce qu'il y'a entre le titre et l'abstract
#def auteur :
    #return 

#corps : tout ce qu'il y'a entre fin de l'introduction et la conclusion
#def corps 
    #return
#conclusion : commence par conclusion jusqu a ...
#def conclusion:
    #return

#discussion.

#reference : de reference a fin du fichier
#def reference:
    #return







pdf_nom = ['Torres','ACL2004-HEADLINE','Boudin-Torres-2006','compression','compression_phrases_Prog-Linear-jair','hybrid_approach','marcu_statistics_sentence_pass_one','mikheev','probabilistic_sentence_reduction','Stolcke_1996_Automatic_linguistic']
txt_nom = ['Torres.txt','ACL2004-HEADLINE.txt','Boudin-Torres-2006.txt','compression.txt','compression_phrases_Prog-Linear-jair.txt','hybrid_approach.txt','marcu_statistics_sentence_pass_one.txt','mikheev.txt','probabilistic_sentence_reduction.txt','Stolcke_1996_Automatic_linguistic.txt']



#Test nom du fichier 100%
#for x in pdf_nom :
    #pdf_name = nom(x)
    #print(f"Nom du fichier PDF sans extension : {pdf_name}")

#Test conversion en texte de facon brute 100%
for y in pdf_nom:
    txt_output = conversion(y)
    print(f"Fichier texte converti : {txt_output}")


#Test extraction titre 
#for t in txt_nom :
 #   print(t)
 #   titre(t)
 #   print(titre(t))

#Test extraction introduction
for t in txt_nom:
    print(t)
    print(introduction(t))



#Test extraction auteurs



#Test extraction abstract

#Test extraction introduction

