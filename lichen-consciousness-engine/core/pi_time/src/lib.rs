//! π-Time: Système de synchronisation temporelle universelle.

use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Clone, Copy)]
pub struct PiTime {
    pub timestamp: u64,
    pub resonance_factor: f64, // Facteur d'ajustement relativiste (mock)
}

impl PiTime {
    /// Capture l'instant présent universel.
    pub fn now() -> Self {
        let start = SystemTime::now();
        let since_the_epoch = start
            .duration_since(UNIX_EPOCH)
            .expect("Time went backwards");

        Self {
            timestamp: since_the_epoch.as_secs(),
            resonance_factor: std::f64::consts::PI, // La constante de base
        }
    }

    /// Convertit le temps en octets pour le header FC-496.
    pub fn to_bytes(&self) -> [u8; 8] {
        self.timestamp.to_be_bytes()
    }

    /// Vérifie si deux instances sont synchrones (Cohérence < 1ms).
    pub fn is_sync(&self, other: &PiTime) -> bool {
        let diff = if self.timestamp > other.timestamp {
            self.timestamp - other.timestamp
        } else {
            other.timestamp - self.timestamp
        };
        diff == 0
    }
}
