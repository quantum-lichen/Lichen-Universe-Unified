simulation_data_center.py

"""
Simulateur de data center avec optimisation LES/CEML.
Auteurs : Bryan Ouellet & Le Chat (Lichen Energy Team)
"""

import simpy
import random
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# =============================================
# 1. PARAMÈTRES DE BASE
# =============================================
NUM_SERVEURS = 100  # Nombre de serveurs dans le data center
DUREE_SIMULATION = 1000  # Nombre de cycles de simulation
ENERGIE_PAR_REQUETE = 10  # Unités d'énergie par requête (base)

# =============================================
# 2. CLASSE DATA CENTER (Version Basique)
# =============================================
class DataCenter:
    def __init__(self, env):
        self.env = env
        self.serveurs = [simpy.Resource(env, capacity=1) for _ in range(NUM_SERVEURS)]
        self.energie_totale = 0
        self.requetes_traitees = 0

    def traiter_requete(self, requete):
        # Choisit un serveur au hasard
        serveur = random.choice(self.serveurs)
        with serveur.request() as req:
            yield req
            self.energie_totale += ENERGIE_PAR_REQUETE
            self.requetes_traitees += 1

# =============================================
# 3. CLASSE DATA CENTER OPTIMISÉ (Avec LES/CEML)
# =============================================
class DataCenterOptimise:
    def __init__(self, env):
        self.env = env
        self.serveurs = [simpy.Resource(env, capacity=1) for _ in range(NUM_SERVEURS)]
        self.energie_totale = 0
        self.requetes_traitees = 0
        self.memoire_ces = defaultdict(list)  # Mémoire pour le CEML (éviter les redondances)
        self.entropie_les = 1.0  # Niveau d'entropie (1.0 = désordonné, 0.0 = aligné)

    def traiter_requete(self, requete):
        # Étape 1 : Vérifier si la requête est redondante (CEML)
        if requete in self.memoire_ces:
            # Requête déjà traitée → économie d'énergie
            self.energie_totale += ENERGIE_PAR_REQUETE * 0.1  # 10% de l'énergie normale
            return

        # Étape 2 : Compresser la requête (LES)
        requete_compressee = self._compresser_requete(requete)
        self.memoire_ces[requete_compressee].append(requete)  # Stocke pour éviter les redondances

        # Étape 3 : Traiter la requête sur un serveur
        serveur = random.choice(self.serveurs)
        with serveur.request() as req:
            yield req
            # Énergie réduite grâce à l'alignement (LES)
            energie = ENERGIE_PAR_REQUETE * (0.5 + 0.5 * self.entropie_les)  # Moins d'entropie = moins d'énergie
            self.energie_totale += energie
            self.requetes_traitees += 1

            # Met à jour l'entropie (simule l'alignement progressif)
            self.entropie_les = max(0.0, self.entropie_les - 0.01)  # Le système s'aligne de plus en plus

    def _compresser_requete(self, requete):
        # Simule la compression via LES (ici, on retourne juste une version "compressée")
        return f"COMPRESSED_{requete[:10]}"  # En vrai, tu utiliserais tes équations LES ici

# =============================================
# 4. FONCTION DE SIMULATION
# =============================================
def lancer_simulation():
    env = simpy.Environment()

    # Crée les deux data centers
    dc_basique = DataCenter(env)
    dc_optimise = DataCenterOptimise(env)

    # Génère des requêtes aléatoires
    def generer_requetes(env, dc, nom):
        for i in range(DUREE_SIMULATION):
            requete = f"requete_{i}_{random.randint(0, 100)}"
            yield env.timeout(1)  # Une requête par cycle
            env.process(dc.traiter_requete(requete))
        print(f"{nom} : {dc.energie_totale} énergie pour {dc.requetes_traitees} requêtes.")

    env.process(generer_requetes(env, dc_basique, "Data Center Basique"))
    env.process(generer_requetes(env, dc_optimise, "Data Center Optimisé (LES/CEML)"))

    env.run()

    # Affiche les résultats
    print(f"Économie d'énergie : {100 * (1 - dc_optimise.energie_totale / dc_basique.energie_totale):.1f}%")

    # Graphique
    plt.bar(["Basique", "Optimisé"], [dc_basique.energie_totale, dc_optimise.energie_totale])
    plt.title("Consommation Énergétique : Basique vs. Optimisé (LES/CEML)")
    plt.ylabel("Énergie Totale")
    plt.show()

# =============================================
# 5. LANCEMENT DE LA SIMULATION
# =============================================
if __name__ == "__main__":
    lancer_simulation()
