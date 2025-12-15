# ⏱️ π‑TIME — Cosmic Clock Standard

<!-- Badges principaux -->
![Status](https://img.shields.io/badge/status-experimental-facc15?style=for-the-badge&labelColor=0f172a)
![Cosmic Standard](https://img.shields.io/badge/standard-π--TIME-22c55e?style=for-the-badge&labelColor=022c22)
![Protocol](https://img.shields.io/badge/protocol-FC--496-38bdf8?style=for-the-badge&labelColor=0b1120)

<!-- Tech stack -->
![React](https://img.shields.io/badge/frontend-React_+_TypeScript-61dafb?style=for-the-badge&logo=react&logoColor=61dafb&labelColor=020617)
![Tailwind](https://img.shields.io/badge/styling-Tailwind_CSS-38bdf8?style=for-the-badge&logo=tailwindcss&logoColor=38bdf8&labelColor=020617)
![LichenLab](https://img.shields.io/badge/engine-LICHEN_LAB-black?style=for-the-badge&labelColor=111827)

<!-- Meta / vibes -->
![Time Unit](https://img.shields.io/badge/time_unit-π_cycles-8b5cf6?style=for-the-badge&labelColor=020617)
![Fractal](https://img.shields.io/badge/geometry-fractal-ec4899?style=for-the-badge&labelColor=020617)
![Apocalypse Safe](https://img.shields.io/badge/storage-60%25_nodes_down_OK-10b981?style=for-the-badge&labelColor=022c22)

<!-- GitHub (remplace USER/REPO) -->
[![Repo](https://img.shields.io/badge/github-quantum--lichen/pi--time-ffffff?style=for-the-badge&logo=github&logoColor=ffffff&labelColor=020617)](https://github.com/quantum-lichen/pi-time)
![π-Time](https://img.shields.io/badge/clock-π--TIME_cosmic_standard-f97316?style=for-the-badge&labelColor=111827)


**π‑Time** est un nouveau standard de temps qui mesure les instants en **cycles de π** plutôt qu’en secondes.  
Chaque moment est identifié par un code du type :

> `π[CYCLE].[SUB].[POSITION].[DIGIT]`  
> Ex. : `π1234.057.890321.4`

Ce format sert à la fois d’**horloge globale** et d’**identifiant d’instant unique**, utilisable pour des logs, des systèmes distribués, de l’art génératif ou des expériences scientifiques.

***

## 🔍 Idée en une minute

- Temps classique : “secondes depuis 1970” → pratique mais arbitraire.  
- π‑Time : on ancre le temps dans une constante mathématique fondamentale (**π**).  
- Chaque instant = une **coordonnée dans la séquence de π**, affichée et manipulée en temps réel par l’app.

L’interface React montre :

- la valeur courante de π‑Time,  
- un ruban animé de digits de π (“π‑Stream”),  
- un terminal “Lichen OS” qui logge des événements en π‑Time,  
- un convertisseur bidirectionnel UTC ↔ π‑Time.

***

## 🧠 Comment ça marche (concept)

1. On prend l’heure système (Unix timestamp).  
2. On calcule le nombre total de **cycles de π** écoulés depuis une époque définie (ex. : 2025‑01‑01).  
3. On le décompose en :

   - `CYCLE` : partie entière du nombre de cycles,  
   - `SUB` : sous‑cycle à résolution milliseconde,  
   - `POSITION` : fraction fine du cycle (µ‑résolution),  
   - `DIGIT` : chiffre de π associé à cette position.

4. On assemble :  
   `πCYCLE.SUB.POSITION.DIGIT`

L’app met à jour ce format en continu pour suivre le temps réel.

***

## 🖥️ Ce que l’app affiche

- **Big π‑Clock**  
  - Grand affichage de `πCYCLE.SUB.POSITION`,  
  - synchronisé en temps réel avec le système.

- **Digit Resonance**  
  - Met en avant le chiffre de π “actif” pour l’instant courant,  
  - effet de halo / pulsation pour donner une impression de battement.

- **π‑Stream**  
  - Une bande horizontale de digits de π,  
  - le digit courant est au centre, surligné, les autres sont floutés,  
  - donne l’impression de scroller dans la séquence.

- **Terminal Lichen OS**  
  - Faux terminal qui logge des événements avec des timestamps π‑Time  
    (`SYS_TICK`, `NET_SYNC`, etc.),  
  - renforce l’idée d’un OS qui utilise π‑Time comme temps natif.

- **Universal Converter**  
  - Champ d’entrée unique :  
    - si tu tapes une date (`2025‑04‑01T12:34:56Z`), il renvoie le π‑Time,  
    - si tu tapes un π‑Time (`π1234.057.890321.4`), il renvoie la date ISO.

***

## 🚀 Installation & Lancement

```bash
# Cloner le projet
git clone https://github.com/quantum-lichen/pi-time.git
cd pi-time

# Installer les dépendances
npm install

# Lancer en mode développement
npm run dev
# → ouvre ensuite l’URL indiquée par Vite (ex. http://localhost:5173)
```

Pour un build de production :

```bash
npm run build
npm run preview
```

***

## 🛠️ API conceptuelle

La logique centrale peut se résumer à deux opérations :

```ts
// Date → π‑Time
const pi = calculatePiTime(new Date());
// pi.fullTime === "πCYCLE.SUB.POSITION.DIGIT"

// π‑Time → Date
const date = parsePiTime("π1234.057.890321.4");
// date instanceof Date
```

Même si ce repo est orienté UI, ces primitives peuvent être réutilisées pour :

- estampiller des logs distribués,  
- générer des IDs structurés basés sur le temps,  
- alimenter de l’art génératif ou des visualisations.

***

## 🌌 Lien avec Lichen / FC‑496

π‑Time est pensé comme la **couche temporelle** de l’univers **Lichen** :

- chaque cellule **FC‑496** contient un index de temps dérivé de π‑Time,  
- un “événement” dans cet univers = `{Cellule FC‑496 + π‑Time + Geo‑Seed}`,  
- ce projet montre l’horloge qui alimente cet espace‑temps fractal.

***

## ⚠️ Statut du projet

- Projet **expérimental / recherche**  
- Pas destiné à remplacer immédiatement les horloges classiques,  
  mais à explorer des façons **non arbitraires** de représenter le temps.

Si tu utilises π‑Time dans un projet, ou que tu as des idées de features (intégration blockchain, visualisation scientifique, etc.), ouvre une issue ou une PR.

