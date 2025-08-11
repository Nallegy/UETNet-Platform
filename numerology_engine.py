import unicodedata
import json

# --- 1. Numerology Mappings ---

# Example Pythagorean numerology map (A=1, B=2... I=9, J=1, ...)
pythagorean_map = {
    **{chr(i+65): ((i % 9) + 1) for i in range(26)},  # Uppercase A-Z
    **{chr(i+97): ((i % 9) + 1) for i in range(26)},  # Lowercase a-z
}

# Example Hebrew gematria mapping (simplified)
hebrew_map = {
    "א": 1, "ב": 2, "ג": 3, "ד": 4, "ה": 5, "ו": 6, "ז": 7, "ח": 8, "ט": 9,
    "י": 10, "כ": 20, "ל": 30, "מ": 40, "נ": 50, "ס": 60, "ע": 70, "פ": 80, "צ": 90,
    "ק": 100, "ר": 200, "ש": 300, "ת": 400
}

# Example Greek isopsephy mapping (simplified)
greek_map = {
    "α": 1, "β": 2, "γ": 3, "δ": 4, "ε": 5, "ϛ": 6, "ζ": 7, "η": 8, "θ": 9,
    "ι": 10, "κ": 20, "λ": 30, "μ": 40, "ν": 50, "ξ": 60, "ο": 70, "π": 80, "ϙ": 90,
    "ρ": 100, "σ": 200, "τ": 300, "υ": 400, "φ": 500, "χ": 600, "ψ": 700, "ω": 800
}

# --- 2. Helpers ---

def normalize_text(text):
    """Strip diacritics and normalize Unicode."""
    nfkd_form = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def digital_root(n):
    """Calculate the digital root of a number."""
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def prime_factor_signature(n):
    """Return prime factorization signature as a dictionary."""
    if n == 0: return {0:1}
    if n == 1: return {1:1}
    factors = {}
    d = 2
    temp_n = n
    while temp_n > 1:
        while temp_n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            temp_n //= d
        d += 1
        if d * d > temp_n and temp_n > 1: # Optimization for large primes
            factors[temp_n] = 1
            break
    return factors

# --- 3. Core Function ---

def numerology_vector(text):
    """Calculate the full numerological vector for a given text."""
    text_norm = normalize_text(text)
    pyth = sum(pythagorean_map.get(ch, 0) for ch in text_norm)
    heb = sum(hebrew_map.get(ch, 0) for ch in text_norm)
    grk = sum(greek_map.get(ch, 0) for ch in text_norm)
    root = digital_root(pyth) if pyth > 0 else 0
    prime_sig = prime_factor_signature(pyth)
    return {
        "text_input": text,
        "pythagorean_sum": pyth,
        "hebrew_gematria": heb,
        "greek_isopsephy": grk,
        "digital_root": root,
        "prime_signature": prime_sig
    }

# --- 4. Glyph Registry Skeleton ---

glyph_registry = [
    {
        "id": "G:KZ-023",
        "char": "ϟ",
        "name": "Greek Koppa variant",
        "origin": "Ancient Greek",
        "morphology": {"strokes": 3, "symmetry": "none"},
        "notes": "Used in numeric contexts as 90 in isopsephy"
    },
    {
        "id": "R:FE-001",
        "char": "ᚠ",
        "name": "Fehu",
        "origin": "Elder Futhark",
        "morphology": {"strokes": 3, "symmetry": "vertical"},
        "notes": "Rune for cattle, wealth"
    }
]