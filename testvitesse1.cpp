#include <iostream>
#include <chrono>

int main() {
    auto temps_debut = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < 1000; i++) {
        for (int j = 0; j < 1000; j++) {
            std::cout << i << std::endl;
            std::cout << j << std::endl;
        }
    }

    auto temps_fin = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> duree_execution = temps_fin - temps_debut;

    std::cout << "Le temps d'exécution de la double boucle est de " << duree_execution.count() << " secondes" << std::endl;

    return 0;
}
//Le temps d'exécution de la double boucle est de 2.68642 secondes