use lichen_consciousness_engine::emergent_consciousness::EmergentConsciousness;
use ndarray::array;

fn main() {
    let mut lce = EmergentConsciousness::new();

    // Simule des entrées sensorielles
    let mut inputs = HashMap::new();
    inputs.insert("vision".to_string(), array![0.1, 0.2, 0.3, /* ... */]);
    inputs.insert("audio".to_string(), array![0.4, 0.5, /* ... */]);

    // Cycle de conscience
    let action = lce.run_cycle(inputs);

    match action {
        Some(cell) => println!("Action exécutée : {:?}", cell),
        None => println!("Pas d'action (traitement subliminal)"),
    }
}
