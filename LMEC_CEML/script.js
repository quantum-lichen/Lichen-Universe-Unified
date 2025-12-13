// LMEC_CEML/script.js

// Constantes
const PHI = 1.618;
// Rayon du cercle dans le SVG (r=45)
const RADIUS = 45;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

// DOM Elements
const coherenceInput = document.getElementById('coherence');
const entropyInput = document.getElementById('entropy');
const valC = document.getElementById('val-c');
const valH = document.getElementById('val-h');
const scoreRing = document.getElementById('score-ring');
const finalScoreEl = document.getElementById('final-score');
const decisionEl = document.getElementById('decision-text');
const fractalBg = document.getElementById('fractal-bg');

// Initialisation du Cercle SVG
scoreRing.style.strokeDasharray = `${CIRCUMFERENCE} ${CIRCUMFERENCE}`;
scoreRing.style.strokeDashoffset = CIRCUMFERENCE; // Commence vide (ou plein selon logique)

// Fonction de calcul CEML
function updateCEML() {
    const C = parseFloat(coherenceInput.value);
    const H = parseFloat(entropyInput.value);

    // Mise à jour des labels textuels
    valC.textContent = C.toFixed(2);
    valH.textContent = H.toFixed(2);

    // ÉQUATION MAÎTRESSE : J = C / (H + epsilon)
    let score = C / (H + 0.001);
    
    // Affichage de la valeur
    finalScoreEl.textContent = score.toFixed(2);

    // --- VISUALISATION DU CERCLE ---
    // On normalise le score pour l'affichage (disons que 5.0 est le "max" visuel pour un cercle plein)
    // Si score = 0 -> offset = CIRCUMFERENCE (vide)
    // Si score = 5 -> offset = 0 (plein)
    const maxVisualScore = 5.0;
    let percent = Math.min(score / maxVisualScore, 1.0);
    const offset = CIRCUMFERENCE - (percent * CIRCUMFERENCE);
    scoreRing.style.strokeDashoffset = offset;

    // --- LOGIQUE DE DÉCISION & COULEURS ---
    if (score >= PHI) {
        // RÉSONANCE
        decisionEl.textContent = "RÉSONANCE";
        decisionEl.style.color = "var(--success)";
        scoreRing.style.stroke = "var(--success)";
        pulseFractal(true);
    } else if (C > 0.8 && H < 0.1) {
        // HALLUCINATION POTENTIELLE
        decisionEl.textContent = "HALLUCINATION ?";
        decisionEl.style.color = "var(--neon-blue)";
        scoreRing.style.stroke = "var(--neon-blue)";
        pulseFractal(false);
    } else {
        // DISSONANCE (Rejet)
        decisionEl.textContent = "DISSONANCE";
        decisionEl.style.color = "var(--danger)";
        scoreRing.style.stroke = "var(--danger)";
        pulseFractal(false);
    }
}

// Animation Fractale de fond (Génération des particules)
function initFractal() {
    for(let i=0; i<80; i++) { // Un peu moins de particules pour alléger
        let div = document.createElement('div');
        div.style.position = 'absolute';
        div.style.width = '3px';
        div.style.height = '3px';
        div.style.background = 'rgba(212, 175, 55, 0.4)';
        div.style.borderRadius = '50%';
        
        // Maths Spirale d'Or
        let angle = i * 137.5 * (Math.PI / 180); 
        let r = 6 * Math.sqrt(i); // Rayon écarté
        
        let x = 50 + r * Math.cos(angle); 
        let y = 50 + r * Math.sin(angle); 
        
        div.style.left = x + '%';
        div.style.top = y + '%';
        div.className = 'fractal-dot';
        
        fractalBg.appendChild(div);
    }
}

function pulseFractal(isResonant) {
    const dots = document.querySelectorAll('.fractal-dot');
    dots.forEach(dot => {
        if(isResonant) {
            dot.style.transform = "scale(1.5)";
            dot.style.boxShadow = "0 0 8px var(--gold)";
            dot.style.opacity = "1";
        } else {
            dot.style.transform = "scale(1)";
            dot.style.boxShadow = "none";
            dot.style.opacity = "0.4";
        }
    });
}

// Listeners
coherenceInput.addEventListener('input', updateCEML);
entropyInput.addEventListener('input', updateCEML);

// Démarrage
initFractal();
// Petit délai pour assurer que le SVG est prêt avant l'anim
setTimeout(updateCEML, 50);
