import React from 'react';
import { LichenNode, PHI } from '../types';
import { Network, Database, Zap, Activity } from 'lucide-react';

interface Props {
  nodes: LichenNode[];
  isQuantumMode: boolean;
  reconstructing: boolean;
}

const Visualizer: React.FC<Props> = ({ nodes, isQuantumMode, reconstructing }) => {
  const centerX = 300;
  const centerY = 300;

  return (
    <div className="relative w-full h-[600px] flex items-center justify-center bg-void overflow-hidden rounded-xl border border-lichen-900 shadow-2xl">
      {/* Background Grid */}
      <div className="absolute inset-0 opacity-20" 
           style={{ backgroundImage: 'radial-gradient(circle, #22c55e 1px, transparent 1px)', backgroundSize: '30px 30px' }}>
      </div>

      {/* Quantum Field Effect */}
      {isQuantumMode && (
        <div className="absolute inset-0 animate-spin-slow opacity-30 pointer-events-none">
          <svg width="100%" height="100%" viewBox="0 0 600 600">
            <circle cx="300" cy="300" r="250" fill="none" stroke="#4ade80" strokeWidth="1" strokeDasharray="10 20" />
            <path d="M300,50 L350,550 M50,300 L550,300" stroke="#4ade80" strokeWidth="0.5" />
          </svg>
        </div>
      )}

      {/* Main SVG */}
      <svg width="100%" height="100%" viewBox="0 0 600 600" className="relative z-10">
        {/* Connection Lines (Synapses) */}
        {nodes.map((node, i) => 
          nodes.slice(i + 1).map((target, j) => {
             // Only draw connection if close enough (Fibonacci neighbors)
             const dist = Math.sqrt(Math.pow(node.x - target.x, 2) + Math.pow(node.y - target.y, 2));
             if (dist > 150) return null;
             
             const isLinkAlive = node.status !== 'dead' && target.status !== 'dead';
             
             return (
               <line 
                key={`link-${i}-${j}`}
                x1={node.x} y1={node.y}
                x2={target.x} y2={target.y}
                stroke={isLinkAlive ? (reconstructing ? '#facc15' : '#14532d') : '#330000'}
                strokeWidth={isLinkAlive ? 1.5 : 0.5}
                className="transition-colors duration-500"
                opacity={isLinkAlive ? 0.6 : 0.2}
               />
             );
          })
        )}

        {/* Nodes */}
        {nodes.map((node) => {
          let fill = '#22c55e';
          let stroke = '#4ade80';
          let r = 18;

          if (node.status === 'dead') {
            fill = '#450a0a';
            stroke = '#7f1d1d';
            r = 14;
          } else if (node.status === 'recovering') {
            fill = '#eab308';
            stroke = '#fef08a';
          } else if (node.status === 'quantum-entangled') {
            fill = '#3b82f6';
            stroke = '#60a5fa';
          }

          return (
            <g key={node.id} className="node-transition">
              {/* Pulse Effect for Active/Recovering */}
              {(node.status === 'active' || node.status === 'recovering') && (
                <circle cx={node.x} cy={node.y} r={r + 8} fill={fill} opacity="0.2">
                  <animate attributeName="r" values={`${r};${r+12};${r}`} dur="2s" repeatCount="indefinite" />
                  <animate attributeName="opacity" values="0.2;0;0.2" dur="2s" repeatCount="indefinite" />
                </circle>
              )}
              
              {/* Core Node */}
              <circle 
                cx={node.x} 
                cy={node.y} 
                r={r} 
                fill={fill} 
                stroke={stroke} 
                strokeWidth="2"
                className="drop-shadow-[0_0_8px_rgba(74,222,128,0.6)]"
              />

              {/* Data Fragment ID */}
              <text 
                x={node.x} 
                y={node.y} 
                dy=".3em" 
                textAnchor="middle" 
                fontSize="10" 
                fill={node.status === 'dead' ? '#7f1d1d' : '#050505'} 
                fontWeight="bold"
                className="font-mono"
              >
                {node.status === 'dead' ? 'ERR' : 'φ'}
              </text>
            </g>
          );
        })}
      </svg>
      
      {/* Overlay Status */}
      <div className="absolute top-4 left-4 font-mono text-xs text-lichen-400">
        <div>TOPO: PHYLLOTAXIS</div>
        <div>THETA: 137.5°</div>
        <div>MOD: 496</div>
      </div>
    </div>
  );
};

export default Visualizer;
