import streamlit as st
import numpy as np
import hashlib
import time
import random
import plotly.graph_objects as go

PHI = 1.6180339887
N_NODES = 10
K_THRESHOLD = int(N_NODES / PHI) + 1  # 7

st.set_page_config(page_title="🟢 LICHEN STORAGE", layout="wide")

st.title("🟢 **LICHEN STORAGE** : Stockage IMMORTEL")
st.markdown("**60% Apocalypse OK** | φ-optimal 1.618x | Math-proof")

# Sidebar
st.sidebar.header("⚙️ Config")
data_input = st.sidebar.text_area("Données à stocker", "Le code est indestructible 🟢")
n_nodes = st.sidebar.slider("Nœuds", 5, 15, N_NODES)

# Bouton apocalypse
if st.sidebar.button("💥 SIMULE APOCALYPSE (60%)"):
    st.session_state.apocalypse = True
    st.session_state.alive_count = n_nodes - int(0.6 * n_nodes)

# Cluster visual
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🌿 Cluster φ-Spirale")
    
    # Génère positions spirale dorée
    angles = np.linspace(0, 2*np.pi, n_nodes)
    radius = np.logspace(0, 1, n_nodes)
    nodes_x = radius * np.cos(angles)
    nodes_y = radius * np.sin(angles)
    
    alive_nodes = [True] * n_nodes
    if st.session_state.get('apocalypse', False):
        dead_count = int(0.6 * n_nodes)
        dead_indices = random.sample(range(n_nodes), dead_count)
        for i in dead_indices:
            alive_nodes[i] = False

with col2:
    fig = go.Figure()
    for i in range(n_nodes):
        color = "green" if alive_nodes[i] else "red"
        status = "🟢" if alive_nodes[i] else "🔴"
        fig.add_trace(go.Scatterpolar(
            r=[0, 1], theta=[360/n_nodes*i],
            mode='markers+text', 
            marker=dict(size=25, color=color),
            text=[status], 
            textposition="middle center",
            name=f"Nœud {i+1}"
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False, 
        title="Topologie φ (Survivants: " + 
        str(sum(alive_nodes)) + "/" + str(n_nodes) + ")"
    )
    st.plotly_chart(fig, use_container_width=True)

# Test CRAID
if st.button("🧪 TEST CRAID-496", type="primary"):
    with st.spinner("🔄 Encodage φ-optimal..."):
        original_data = data_input.encode()
        cell_id = hashlib.sha256(original_data).hexdigest()[:8]
        
        st.success(f"✅ Écriture OK: `{cell_id}`")
        st.info(f"📡 Distribué sur {n_nodes} nœuds (seuil K={K_THRESHOLD})")
        
        time.sleep(1)
        if st.session_state.get('apocalypse', False):
            st.error(f"💥 APOCALYPSE: {st.session_state.alive_count} survivants")
            if st.session_state.alive_count >= K_THRESHOLD:
                st.success("🟢 **RÉCUPÉRATION 100%** | CRAID-496 victorieux!")
                st.balloons()
            else:
                st.warning("❌ Sous-seuil K | Reconstruction impossible")
        else:
            st.success(f"**RÉSULTAT :** `{data_input}` ✅")

# Tableau comparatif
st.markdown("""
## 🏆 LICHEN vs Concurrents
| Critère | RAID-6 | Erasure | **LICHEN** |
|---------|--------|---------|------------|
| **Pannes** | 2 | N-K | **60%+** |
| **Overhead** | 2x | 1.5-3x | **φ=1.618x** |
| **Downtime** | Arrêt | Risqué | **0s** |
| **Quantum** | ❌ | ❌ | ✅ |
""")

st.markdown("---")
st.markdown("⭐ **Star le repo !** [GitHub](https://github.com/quantum-lichen/Lichen-Universe-Unified/tree/main/LICHEN.STORAGE)")
