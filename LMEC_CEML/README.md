# Cognitive Entropy Minimization Law (CEML)
## Loi de Minimisation de l’Entropie Cognitive (LMC)

**A Candidate Selection Principle for Intelligent Systems**
*Un principe candidat de sélection pour les systèmes intelligents*

---

## 1. Overview / Vue d’ensemble

### 🇬🇧 English
**CEML** proposes a simple but operational principle: an intelligent system should preferentially select informational structures that strongly align with the current context while minimizing their entropic cost.

This principle formalizes a fundamental trade-off implicit in cognition, learning, and inference: **Contextual Coherence vs. Informational Complexity**.

### 🇫🇷 Français
La **LMC** formalise une intuition simple : un système intelligent devrait préférer les structures d’information fortement cohérentes avec le contexte, tout en restant aussi peu coûteuses que possible en termes entropiques.

Cette loi explicite un compromis fondamental déjà présent dans la cognition et l’apprentissage : **Cohérence Contextuelle vs Coût Informationnel**.

---

## 2. Mathematical Formulation / Formulation Mathématique

### 2.1 Canonical Form / Forme Canonique
The core objective function determines the fitness score $J(s)$ of a candidate structure $s$:

$$J(s) = \frac{\mathcal{C}(s \mid \Omega)}{\mathcal{H}(s) + \epsilon}$$

**Definitions:**
* $s$: The candidate structure (e.g., a token sequence, a thought, a memory).
* $\Omega$: The external context or ground truth.
* $\mathcal{C}(s \mid \Omega)$: **Contextual Coherence**. Represents the semantic alignment or utility.
* $\mathcal{H}(s)$: **Entropic Cost**. Represents Shannon entropy, complexity, or metabolic cost.
* $\epsilon$: A strictly positive regularization constant ($\epsilon > 0$).
* $s^* = \arg\max_s J(s)$: The selected optimal structure.

### 2.2 Regularized Fractal Form / Forme Fractale Régularisée
To improve numerical stability and allow for scale-dependent behaviors (fractal cognition), we introduce tuning parameters $\alpha$ and $\beta$:

$$J_{\alpha,\beta}(s) = \frac{\mathcal{C}(s \mid \Omega)^{\alpha}} {\left(\mathcal{H}(s) + \epsilon\right)^{\beta}}$$

* $\alpha$ (Alpha): Controls **Selectivity** (sensitivity to context).
* $\beta$ (Beta): Controls **Compression Pressure** (sensitivity to complexity).

This generalized form allows the system to adapt its regime (e.g., favoring exploration with low $\beta$, or strict efficiency with high $\beta$).

---

## 3. Critical Clarification / Clarification Importante

> **⚠️ Truth $\neq$ Coherence**
>
> **English:** CEML describes a **selection preference** under constraints, not an epistemic guarantee of truth. A structure can have high coherence (fit the context perfectly) yet be factually false if the context itself is biased. It optimizes for *plausibility and efficiency*.
>
> **Français:** La LMC décrit une **préférence de sélection** sous contraintes, et non une garantie de vérité. Une structure peut avoir une haute cohérence (coller parfaitement au contexte) tout en étant factuellement fausse si le contexte est lui-même biaisé. Elle optimise *la plausibilité et l'efficacité*.

---

## 4. Cognitive Regimes / Régimes Cognitifs

The ratio $C/H$ naturally defines four qualitative regimes of operation:

| Regime | Coherence $\mathcal{C}$ | Entropy $\mathcal{H}$ | Interpretation |
| :--- | :---: | :---: | :--- |
| **Resonance** | **High** | **Low** | **Optimal State.** Stable, efficient, and aligned cognition. |
| **Dissonance** | Low | Low | Rigid structure, but misaligned with context. |
| **Chaos** | Low | High | Noisy, unstable cognition. High energy, zero utility. |
| **Hallucination** | *High (Local)* | *Misestimated* | Fragile state. Overconfident but often statistically abnormal. |

---

## 5. Operational Pipeline / Pipeline Opérationnel

CEML acts as a filter in the cognitive pipeline:

$$\text{Generation} \rightarrow \text{CEML Evaluation } J(s) \rightarrow \text{Selection} (s^*) \rightarrow \text{Memory/Action}$$

### Applications
1.  **LLM Decoding:** Use $J(s)$ as a re-ranking criterion for beam search, favoring answers that balance relevance and conciseness.
2.  **Memory Pruning:** Only store memories (FC-496 cells) that maintain a high $J$ score over time.
3.  **Trajectory Stability:** Monitor $J(s)$ over time to detect if a system is drifting into *Chaos* or *Dissonance*.

---

## 6. Proof of Concept

A Python implementation validates the behavior of the law on probability distributions.

**Script:** `docs/ceml/CEML_demo_distributions.py`

**Results Summary:**
* **Highly Ordered Distributions:** Yield maximal CEML scores.
* **Uniform Distributions:** Yield minimal scores.
* **Behavior:** The score decays monotonically as entropy increases (assuming constant coherence).

---

## 7. Status & Context

**Position within the Universe:**
* **UICT (Unified Information Compression Theory):** Describes global informational dynamics (Physics).
* **CEML (Cognitive Entropy Minimization Law):** Describes local selection rules (Mind).

**Disclaimer:**
This is a **theoretical framework** proposed for the design and analysis of cognitive architectures. It is compatible with the Free Energy Principle (Friston) and Minimum Description Length (MDL), but remains a candidate model for experimental validation.
