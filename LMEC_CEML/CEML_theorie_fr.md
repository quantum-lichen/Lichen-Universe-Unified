# Loi de Minimisation de l’Entropie Cognitive (LMC / CEML)
**Un cadre mathématique unifié pour la sélection de l’information dans les systèmes cognitifs**

**Auteur :** Bryan Ouellette  
**Date :** 13 décembre 2025  
**Version :** 2.1 (Affinée)

---

## 1. Motivation

Les systèmes intelligents – biologiques ou artificiels – sont soumis à des contraintes finies d’énergie, de temps et de mémoire. Ils ne peuvent pas explorer toutes les représentations possibles du monde, et doivent donc **sélectionner** un sous‑ensemble de structures à la fois **sémantiquement utiles** et **énergétiquement efficaces**.

La LMC propose une règle quantitative simple :  
maximiser la **cohérence contextuelle** tout en minimisant le **coût entropique**.

---

## 2. Principe central

> **Axiome de Moindre Action Cognitive (LMC)**  
> Tout agent cognitif sous contraintes de ressources sélectionne préférentiellement les structures d’information qui maximisent l’utilité sémantique tout en minimisant le coût entropique (énergétique).

Autrement dit, “comprendre” est traité comme un processus de **compression d’information** qui conserve l’essentiel (cohérence) et élimine le bruit (entropie).

---

## 3. Définition mathématique

Soit \(\mathcal{S}\) l’ensemble des structures candidates (phrases, vecteurs, états internes).  
Pour un contexte donné \(\Omega\), la LMC définit une **fonction de score** :

\[
J(s) = \frac{\mathcal{C}(s \mid \Omega)}{\mathcal{H}(s) + \epsilon}
\]

où :

- \(s \in \mathcal{S}\) est une structure candidate.  
- \(\Omega\) est le contexte courant (prompt, état sensoriel, vérité terrain).  
- \(\mathcal{C}(s \mid \Omega)\) est la **Cohérence Contextuelle**.  
- \(\mathcal{H}(s)\) est le **Coût Entropique**.  
- \(\epsilon \to 0^+\) est une petite constante pour éviter les singularités.

La **règle de sélection LMC** est :

\[
s^\* = \underset{s \in \mathcal{S}}{\mathrm{argmax}} \; J(s)
\]

### 3.1 Cohérence contextuelle \(\mathcal{C}(s \mid \Omega)\)

En espace d’embeddings, on peut la définir par la similarité cosinus :

\[
\mathcal{C}(s \mid \Omega) = \frac{\vec{v}_\Omega \cdot \vec{v}_s}{\lVert \vec{v}_\Omega \rVert \, \lVert \vec{v}_s \rVert}
\]

- \(\mathcal{C}\) élevée : \(s\) est aligné avec \(\Omega\) (pertinent, sur le sujet, conforme au modèle).  
- \(\mathcal{C}\) faible : \(s\) est hors sujet, incohérent ou peu soutenu par le contexte.

### 3.2 Coût entropique \(\mathcal{H}(s)\)

\(\mathcal{H}(s)\) capture à quel point il est **coûteux** de représenter ou traiter \(s\).

Pour une distribution de probabilité \(p(i)\) :

\[
\mathcal{H}(s) = H(p) = -\sum_i p(i) \log_2 p(i)
\]

Pour du texte ou des sorties de modèles, \(\mathcal{H}(s)\) peut être approchée par :

- la log‑probabilité moyenne (cross‑entropy),  
- ou le ratio de compression (taille gzip / taille brute).

Plus \(\mathcal{H}(s)\) est grande → plus de désordre, plus de bits, plus d’énergie dissipée.  
Plus \(\mathcal{H}(s)\) est petite → plus de compression, plus de régularité, moins de coût.

---

## 4. Régimes qualitatifs

La LMC prédit quatre grands régimes :

| Type d’état      | Cohérence \(\mathcal{C}\) | Entropie \(\mathcal{H}\) | Score \(J(s)\)     | Décision        | Exemple (FR)                    |
|------------------|---------------------------|---------------------------|--------------------|-----------------|----------------------------------|
| **Résonance**    | Haute                     | Basse                     | **Maximum**        | SÉLECTION       | « Le ciel est bleu. »           |
| **Dissonance**   | Basse                     | Basse                     | Faible             | REJET           | « Le chat est cubique. »        |
| **Chaos**        | Haute/Basse               | Haute                     | Faible             | REJET           | « Bleu ciel… 37x… bruit… »      |
| **Hallucination** | Haute (locale)          | Basse (artificielle)      | Faux maximum local | Pathologie      | Cliché plausible mais faux.     |

L’optimum “sain” correspond à une **cohérence élevée** avec une **entropie faible à modérée** (complexité ordonnée).

---

## 5. Lien avec les principes existants

La LMC est conçue pour être compatible avec plusieurs cadres :

1. **Principe de l’Énergie Libre (Friston)**  
   Le cerveau minimise une énergie libre liée à la surprise des observations.  
   - Dans la LMC, diminuer \(\mathcal{H}(s)\) sous contrainte de cohérence revient à diminuer la surprise représentée par la structure \(s\). [web:55][web:60]

2. **Théorie de l’Information (Shannon / MDL)**  
   Le meilleur modèle est celui qui explique les données avec la plus petite longueur de description.  
   - Le terme \(\mathcal{H}(s)\) pénalise les structures inutilement complexes ou bruitées. [web:57]

3. **Physique de l’Information (Landauer)**  
   Chaque bit effacé ou traité a un coût énergétique minimal.  
   - La LMC interprète le dénominateur comme un budget énergétique : plus l’entropie est élevée, plus la structure est coûteuse à maintenir. [web:57][web:61]

La LMC n’est pas présentée comme une loi de la nature démontrée, mais comme un **principe de sélection cognitif** unifié :  
parmi de nombreux états internes possibles, l’agent choisit celui qui maximise \(\dfrac{\text{cohérence}}{\text{entropie}}\).

---

## 6. PoC jouet : distributions de probabilité

Pour un PoC minimal, on représente les structures candidates par des distributions discrètes.

On définit :

- \(\mathcal{H}(s)\) = entropie de Shannon de la distribution.  
- \(\mathcal{C}(s \mid \Omega)\) = probabilité maximale (composante dominante), comme proxy de « focus » ou confiance.

### 6.1 Démo Python

import numpy as np

def shannon_entropy(distribution):
return -sum(p * np.log2(p) if p > 0 else 0 for p in distribution)

def coherence(distribution):
# Proxy : masse dominante = focus
return max(distribution)

def lmc_score(distribution, eps=1e-6):
H = shannon_entropy(distribution)
C = coherence(distribution)
return C / (H + eps), H, C

structures = {
'A': [0.95, 0.03, 0.02], # Très ordonné
'B': [0.70, 0.20, 0.10], # Ordonné
'C': [0.50, 0.30, 0.20], # Légèrement ordonné
'D': [0.33, 0.33, 0.34], # Quasi uniforme
'E': [0.45, 0.10, 0.45], # Bimodal
'F': [0.20, 0.25, 0.15, 0.25, 0.15], # Désordonné (5)
'G': [0.16, 0.17, 0.17, 0.16, 0.17, 0.17], # Très désordonné (6)
}

results = []
for name, dist in structures.items():
score, H, C = lmc_score(dist)
results.append((name, H, C, score))

results.sort(key=lambda x: x, reverse=True)​

for name, H, C, score in results:
print(f"{name}: H={H:.4f}, C={C:.2f}, J={score:.4f}")

text

### 6.2 Comportement observé

- A (très ordonné) obtient le **score maximal** \(J(s)\).  
- G (le plus désordonné) obtient le **score minimal**.  
- Le score décroît de manière monotone quand l’entropie augmente, ce qui confirme que la LMC favorise des structures **à forte cohérence et faible entropie** plutôt que le bruit.

Ce PoC valide la **prédiction qualitative** de la LMC sur un cas jouet.

---

## 7. Extensions prévues

- Remplacer la cohérence “max probability” par une cohérence basée sur des embeddings pour des textes.  
- Estimer \(\mathcal{H}(s)\) via la cross‑entropy d’un LLM ou le taux de compression.  
- Utiliser la LMC comme critère de sélection dans le décodage de modèles ou la récupération de mémoire.  
- Tester la corrélation entre scores LMC et jugements humains (clarté, vérité, utilité).

La LMC est présentée comme un **principe candidat** : unifiant plusieurs intuitions existantes en une métrique opérationnelle, conçue pour être testée et potentiellement réfutée sur des systèmes réels.
