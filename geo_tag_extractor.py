import json
import pycountry
import re
from collections import defaultdict

# Βήμα 1: Φόρτωση JSON αρχείου εισόδου
with open("samples_without_geo.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Βήμα 2: Δημιουργία λίστας με επίσημα ονόματα χωρών
country_names = set(country.name for country in pycountry.countries)

# Regex pattern με όλες τις χώρες
country_pattern = re.compile(
    r'\b(?:' + '|'.join(re.escape(name) for name in sorted(country_names, key=len, reverse=True)) + r')\b',
    re.IGNORECASE
)

# Βήμα 3: Ανίχνευση χωρών σε όλα τα πεδία κάθε εγγραφής
geo_hits = defaultdict(lambda: defaultdict(list))

for registry in data:
    for field, value in registry.items():
        if isinstance(value, str) and value.strip():
            matches = country_pattern.findall(value)
            for match in matches:
                match_clean = match.strip()
                if len(geo_hits[match_clean][field]) < 5:
                    geo_hits[match_clean][field].append(value.strip()[:200])

# Βήμα 4: Αποθήκευση αποτελεσμάτων
results = []

for country, field_map in geo_hits.items():
    for field, examples in field_map.items():
        results.append({
            "country": country,
            "field": field,
            "examples": examples
        })

# Εγγραφή σε json
with open("detected_country_keywords.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("✅ Το αρχείο 'detected_country_keywords.json' δημιουργήθηκε με επιτυχία.")