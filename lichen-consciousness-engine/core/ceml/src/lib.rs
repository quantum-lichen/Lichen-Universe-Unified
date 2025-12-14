//! CEML: Cognitive Entropy Minimization Law.
//! Filtre les états cognitifs basés sur leur entropie de Shannon et leur cohérence structurelle.

/// Seuil critique (Ratio d'or inverse).
const PHI_INVERSE: f32 = 0.61803398875;

/// Analyse un vecteur d'état et retourne son score de réalité.
pub fn analyze_state(state_vector: &[f64]) -> f32 {
    let entropy = calculate_shannon_entropy(state_vector);
    let coherence = calculate_structural_coherence(state_vector);
    
    // Formule simplifiée de CEML : Cohérence / (1 + Entropie)
    let score = coherence / (1.0 + entropy);
    
    // Normalisation (clamp entre 0.0 et 1.0)
    score.clamp(0.0, 1.0)
}

/// Vérifie si l'état passe le filtre de réalité.
pub fn is_valid_thought(score: f32) -> bool {
    score >= PHI_INVERSE
}

fn calculate_shannon_entropy(data: &[f64]) -> f32 {
    // Mock simple pour l'exemple
    // Plus les données sont uniformes, plus l'entropie est haute
    let sum: f64 = data.iter().sum();
    if sum == 0.0 { return 0.0; }
    
    data.iter()
        .map(|&x| {
            let p = x / sum;
            if p > 0.0 { -p * p.log2() } else { 0.0 }
        })
        .sum::<f64>() as f32
}

fn calculate_structural_coherence(data: &[f64]) -> f32 {
    // Simulation : vérifie la variance (une variance contrôlée = meilleure cohérence)
    let mean = data.iter().sum::<f64>() / data.len() as f64;
    let variance = data.iter().map(|value| {
        let diff = mean - *value;
        diff * diff
    }).sum::<f64>() / data.len() as f64;

    (1.0 / (1.0 + variance)) as f32
}
