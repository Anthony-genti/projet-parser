import time

# Commencez à mesurer le temps
temps_debut = time.time()

# Votre double boucle ici
for i in range(1000):
    for j in range(1000):
        print(i)
        print(j)

# Arrêtez de mesurer le temps
temps_fin = time.time()

# Calculez la durée totale d'exécution
duree_execution = temps_fin - temps_debut

print("Le temps d'exécution de la double boucle est de", duree_execution, "secondes")
#Le temps d'exécution de la double boucle est de 3.200305461883545 secondes