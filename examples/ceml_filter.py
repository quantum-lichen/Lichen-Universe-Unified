from ceml import compute_ceml

outputs = [
    "Coherent and grounded response.",
    "Incoherent hallucinated speculation."
]

THRESHOLD = 0.618

for text in outputs:
    score = compute_ceml(text)
    if score >= THRESHOLD:
        print(f"[ACCEPTED] {text}")
    else:
        print(f"[FLAGGED] {text}")
