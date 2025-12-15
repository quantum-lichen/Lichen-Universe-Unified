"""
fc496.py – Fractal Cell‑496 (FC‑496) core primitives.

Status: experimental / research
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import json
import math
import time
import os

# ---------------------------------------------------------------------------
#  Constants & basic helpers
# ---------------------------------------------------------------------------

FC496_BITS = 496
MAJOR_BITS = 306          # ≈ 496 / φ
MINOR_BITS = FC496_BITS - MAJOR_BITS  # 190

PHI = (1 + 5 ** 0.5) / 2   # Nombre d'Or
PI = math.pi


def _to_bits(data: bytes) -> str:
    """Convert bytes → bitstring."""
    return "".join(f"{b:08b}" for b in data)


def _from_bits(bits: str) -> bytes:
    """Convert bitstring → bytes (pad to multiple of 8)."""
    if len(bits) % 8 != 0:
        bits = bits.ljust((len(bits) + 7) // 8 * 8, "0")
    return int(bits, 2).to_bytes(len(bits) // 8, "big")


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
#  π‑Time and Geo‑Seed
# ---------------------------------------------------------------------------

def pi_time_from_unix(ts: Optional[float] = None, precision: int = 9) -> str:
    """
    Very simple π‑Time surrogate:
    - Take Unix timestamp
    - Express as integer + fractional, and format as πXXXXXXXX.XXXXXXXXX
    This is a placeholder for a richer mapping based on digits of π.
    """
    if ts is None:
        ts = time.time()
    integer = int(ts)
    frac = ts - integer
    return f"π{integer}.{int(frac * (10 ** precision)):0{precision}d}"


def geo_seed(lat: float, lon: float, extra: str = "") -> str:
    """
    Compute a Geo‑Seed hash from (lat, lon) + optional extra tag.
    In vrai système, ça mapperait sur un maillage fractal (icosaèdre / octogone).
    Ici: SHA‑256(lat|lon|extra) → 64 hex chars.
    """
    payload = f"{lat:.8f}|{lon:.8f}|{extra}".encode("utf-8")
    return _sha256_hex(payload)


# ---------------------------------------------------------------------------
#  FC‑496 Cell model
# ---------------------------------------------------------------------------

@dataclass
class FC496Cell:
    """
    Représente une cellule FC‑496 déjà encodée.
    - bits : string de 496 bits
    - meta  : infos humaines utiles (π‑Time, Geo‑Seed, etc.)
    """
    bits: str
    pi_time: str
    geo_seed: str
    type_tag: str = "generic"
    ceml: Optional[float] = None
    h_scale: Optional[float] = None

    # ------------------------------------------------------------------ #
    #  Basic consistency checks                                          #
    # ------------------------------------------------------------------ #

    def validate_length(self) -> bool:
        return len(self.bits) == FC496_BITS

    def major_bits(self) -> str:
        return self.bits[:MAJOR_BITS]

    def minor_bits(self) -> str:
        return self.bits[MAJOR_BITS:]

    # ------------------------------------------------------------------ #
    #  Phi‑Bond (very simple heuristic)                                  #
    # ------------------------------------------------------------------ #

    def phi_bond_score(self, other: "FC496Cell") -> float:
        """
        Phi‑Bond = mesure de “résonance” entre deux cellules.
        Ici: on calcule la similarité de Hamming sur le Minor Segment,
        puis on la projette dans [0,1] et on regarde si elle est proche de 1/φ.
        """
        a = self.minor_bits()
        b = other.minor_bits()
        if len(a) != len(b):
            return 0.0
        matches = sum(x == y for x, y in zip(a, b))
        sim = matches / len(a)
        # On aime bien quand sim ≈ 1/φ ≈ 0.618
        target = 1.0 / PHI
        return 1.0 - abs(sim - target)

    def can_bond_with(self, other: "FC496Cell", threshold: float = 0.8) -> bool:
        """
        Deux cellules se lient si leur phi_bond_score dépasse un seuil.
        Dans un vrai système, on ajouterait d’autres contraintes.
        """
        return self.phi_bond_score(other) >= threshold


# ---------------------------------------------------------------------------
#  Encoder / Decoder (Transmuter‑lite)
# ---------------------------------------------------------------------------

class FC496Encoder:
    """
    Transmuter simplifié:
    - sérialise un objet Python (dict, list, etc.) en JSON canonique
    - calcule π‑Time + Geo‑Seed
    - répartit dans Major / Minor segments
    - ajoute éventuellement un code de redondance simple

    Ce n’est PAS une implémentation complète de Reed‑Solomon, mais
    l’API est pensée pour en accueillir une plus tard.
    """

    def __init__(
        self,
        default_lat: float = 0.0,
        default_lon: float = 0.0,
        type_tag: str = "generic",
    ):
        self.default_lat = default_lat
        self.default_lon = default_lon
        self.type_tag = type_tag

    # --------------------- public API --------------------------------- #

    def encode_object(
        self,
        obj: Any,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        ceml: Optional[float] = None,
        h_scale: Optional[float] = None,
        pi_ts: Optional[float] = None,
    ) -> FC496Cell:
        """
        Encode un objet arbitraire → une cellule FC‑496.
        Si l’objet est trop gros pour tenir dans 306 bits → il faut
        normalement le sharder sur plusieurs cellules; ici, on tronque.
        """
        lat = self.default_lat if lat is None else lat
        lon = self.default_lon if lon is None else lon

        # 1) sérialisation canonique
        payload_json = self._canonical_json(obj)
        payload_bytes = payload_json.encode("utf-8")
        payload_bits_full = _to_bits(payload_bytes)

        # 2) Major segment = payload + hash, tronqué
        payload_hash = _sha256_hex(payload_bytes)[:16]  # 64 bits hex → 16 hex chars
        payload_hash_bits = bin(int(payload_hash, 16))[2:].zfill(64)

        major_raw = payload_bits_full + payload_hash_bits
        major_bits = major_raw[:MAJOR_BITS].ljust(MAJOR_BITS, "0")

        # 3) Minor segment = π‑Time + Geo‑Seed + meta flags
        pi_str = pi_time_from_unix(pi_ts)
        geo = geo_seed(lat, lon)

        minor_bits = self._encode_minor_segment(
            pi_str,
            geo,
            type_tag=self.type_tag,
            ceml=ceml,
            h_scale=h_scale,
        )

        # 4) Assemblage cellule
        bits = major_bits + minor_bits
        cell = FC496Cell(
            bits=bits,
            pi_time=pi_str,
            geo_seed=geo,
            type_tag=self.type_tag,
            ceml=ceml,
            h_scale=h_scale,
        )
        if not cell.validate_length():
            raise ValueError(f"FC‑496 length mismatch: {len(bits)} != {FC496_BITS}")
        return cell

    def decode_object(self, cell: FC496Cell) -> Dict[str, Any]:
        """
        Décodage “meilleur effort”:
        - extrait le Major segment
        - enlève les 64 bits hash
        - tente de reconstruire le JSON
        Renvoie un dict avec :
          - "data" : objet décodé (ou None)
          - "hash_ok" : bool
          - "raw_json" : string brute utilisée
        """
        major = cell.major_bits()
        if len(major) < 64:
            raise ValueError("Major segment too small")

        # Derniers 64 bits = hash
        payload_bits = major[:-64]
        hash_bits = major[-64:]

        payload_bytes = _from_bits(payload_bits)
        raw_json = payload_bytes.decode("utf-8", errors="ignore").rstrip("\x00")

        try:
            data_obj = json.loads(raw_json)
        except Exception:
            data_obj = None

        recomputed_hash = _sha256_hex(raw_json.encode("utf-8"))[:16]
        recomputed_hash_bits = bin(int(recomputed_hash, 16))[2:].zfill(64)
        hash_ok = (hash_bits == recomputed_hash_bits)

        return {
            "data": data_obj,
            "hash_ok": hash_ok,
            "raw_json": raw_json,
        }

    # --------------------- internal helpers --------------------------- #

    def _canonical_json(self, obj: Any) -> str:
        """JSON stable : clés triées, pas d’espaces; facilite les checksums."""
        return json.dumps(obj, sort_keys=True, separators=(",", ":"))

    def _encode_minor_segment(
        self,
        pi_time_str: str,
        geo_seed_hex: str,
        type_tag: str,
        ceml: Optional[float],
        h_scale: Optional[float],
    ) -> str:
        """
        Encode π‑Time, Geo‑Seed, type_tag et quelques floats en 190 bits.
        Schéma simple:

        -  64 bits : hash(π‑Time) prefix
        -  64 bits : hash(Geo‑Seed) prefix
        -  16 bits : type_tag hash prefix
        -  16 bits : CEML (0..1) quantifié
        -  16 bits : H‑Scale (0..1) quantifié
        - reste   : padding
        """
        # π‑Time hash
        pi_hash = _sha256_hex(pi_time_str.encode("utf-8"))[:16]
        pi_bits = bin(int(pi_hash, 16))[2:].zfill(64)

        # Geo‑Seed hash
        geo_prefix = geo_seed_hex[:16]
        geo_bits = bin(int(geo_prefix, 16))[2:].zfill(64)

        # Type tag (16 bits)
        t_hash = _sha256_hex(type_tag.encode("utf-8"))[:4]
        t_bits = bin(int(t_hash, 16))[2:].zfill(16)

        # CEML / H‑Scale quantized
        def q16(x: Optional[float]) -> str:
            if x is None:
                return "0" * 16
            v = max(0.0, min(1.0, float(x)))
            return f"{int(v * 65535):016b}"

        ceml_bits = q16(ceml)
        h_bits = q16(h_scale)

        raw = pi_bits + geo_bits + t_bits + ceml_bits + h_bits
        return raw[:MINOR_BITS].ljust(MINOR_BITS, "0")


# ---------------------------------------------------------------------------
#  Simple “graph” of cells for Phi‑Bond experiments
# ---------------------------------------------------------------------------

class FC496Graph:
    """
    Graphe très simple de cellules liées par Phi‑Bonds.
    """

    def __init__(self, cells: Optional[List[FC496Cell]] = None):
        self.cells: List[FC496Cell] = cells or []
        # edges[(i,j)] = phi_score
        self.edges: Dict[Tuple[int, int], float] = {}

    def add_cell(self, cell: FC496Cell) -> int:
        self.cells.append(cell)
        return len(self.cells) - 1

    def compute_phi_bonds(self, threshold: float = 0.8) -> None:
        self.edges.clear()
        n = len(self.cells)
        for i in range(n):
            for j in range(i + 1, n):
                s = self.cells[i].phi_bond_score(self.cells[j])
                if s >= threshold:
                    self.edges[(i, j)] = s

    def bonded_components(self) -> List[List[int]]:
        """
        Composantes connexes via Phi‑Bonds (très simple BFS).
        """
        visited = set()
        adj: Dict[int, List[int]] = {i: [] for i in range(len(self.cells))}
        for (i, j), _ in self.edges.items():
            adj[i].append(j)
            adj[j].append(i)

        comps: List[List[int]] = []
        for i in range(len(self.cells)):
            if i in visited:
                continue
            stack = [i]
            comp = []
            while stack:
                u = stack.pop()
                if u in visited:
                    continue
                visited.add(u)
                comp.append(u)
                stack.extend(adj[u])
            comps.append(comp)
        return comps


# ---------------------------------------------------------------------------
#  Demo / CLI usage
# ---------------------------------------------------------------------------

def demo() -> None:
    """
    Petit exemple d’usage: encode 3 objets, construit un graphe, montre les bonds.
    """
    encoder = FC496Encoder(default_lat=45.5017, default_lon=-73.5673, type_tag="demo")

    objs = [
        {"id": "A", "type": "medical_record", "value": 42},
        {"id": "B", "type": "medical_record", "value": 43},
        {"id": "C", "type": "log_entry", "msg": "hello"},
    ]

    cells: List[FC496Cell] = []
    for o in objs:
        cell = encoder.encode_object(o, ceml=0.95, h_scale=0.9)
        cells.append(cell)

    graph = FC496Graph(cells)
    graph.compute_phi_bonds(threshold=0.7)

    print("=== FC‑496 demo ===")
    for i, cell in enumerate(cells):
        decoded = encoder.decode_object(cell)
        print(f"\nCell {i}: type={cell.type_tag}, pi_time={cell.pi_time}")
        print("  hash_ok:", decoded["hash_ok"])
        print("  data   :", decoded["data"])

    print("\nPhi‑Bonds edges (i, j, score):")
    for (i, j), s in graph.edges.items():
        print(f"  ({i}, {j}) -> {s:.3f}")

    print("\nBonded components:", graph.bonded_components())


if __name__ == "__main__":
    demo()
