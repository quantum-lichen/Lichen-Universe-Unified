import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

# ====== Paramètres ======
NUM_SERVEURS = 100
DUREE_SIMULATION = 1000
ENERGIE_PAR_REQUETE = 10

# ====== Tes vraies équations LES ======
def calculer_entropie_les(texte):
    motifs = ["qubit", "spin", "kuramoto", "fc-496", "craid"]
    p = [texte.lower().count(motif)/len(texte) for motif in motifs]
    p = [max(x, 1e-10) for x in p]
    p = [x/sum(p) for x in p]
    return min(-sum(x*np.log2(x) for x in p if x>0), 1.0)

def compresser_requete_les(texte, entropie):
    if entropie > 0.7:
        return f"COMP_{texte[:5]}"
    else:
        mots_cles = [m for m in ["qubit","spin","fc-496"] if m in texte.lower()]
        return "_".join(mots_cles)[:20] if mots_cles else f"UNK_{texte[:5]}"

# ====== Tes vraies équations CEML ======
def detecter_redondance_ceml(texte, memoire):
    signature = compresser_requete_les(texte, 0.5)
    return signature in mem
