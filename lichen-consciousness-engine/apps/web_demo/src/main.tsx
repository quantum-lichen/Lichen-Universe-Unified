import React from 'react';
import { PiTimeClock } from './components/PiTimeClock';

const App: React.FC = () => {
  return (
    <div style={{ textAlign: 'center' }}>
      <h1>🌌 Lichen Consciousness Engine</h1>
      <p>Démo interactive du système de temps universel π-Time et de FC-496.</p>
      <PiTimeClock />
    </div>
  );
};

export default App;
