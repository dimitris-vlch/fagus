# Το παρακάτων script σκανάρει το αρχείο json samples_without_geo.json, λέξη-λέξη, για να εντοπίσει λέξεις-κλειδιά με γεωγραφική πληροφορία. Τις χώρες που βρίσκει, τις καταγράφει σε json αρχειο detected_country_keywords.json, μαζί με τα πεδία όπου εντόπισε τις λέξεις αυτές.

# Βήμα 1: Εισαγωγή βιβλιοθηκών. Εισάγουμε την γνωστή βιβλιοθήκη json αλλά και άλλες.

# Η βιβλιοθήκη pycountry δίνει ονόματα χωρών σε ISO format. France, Germany, Greece, United States κλπ. Έτσι, έχουμε ενα πλήρες λεξικό χωρών για να ψάξουμε λέξεις κλειδιά με γεωγραφική πληροφορία.

# Βιβλιοθήκη re για regular expressions. Χρησιμοποιείται σε περιπτώσεις που θέλουμε να κάνουμε αναζήτηση για λέξεις-κλειδιά, μοτίβα, συγκεκριμένες φράσεις. Θα τη χρησιμοποιήσουμε για να σκανάρουμε τα πεδία, ώστε να βρούμε εαν αυτά περιέχουν ονόματα χωρών.

# from collections import defaultdict
    
    #   Από την βιβλιοθήκη collections, εισάγουμε την ειδική δομή defaultdict, η οποία και συνιστά παραλλαγή του απλού  dict. H defauldict δημιουργεί αυτόματα τιμές για κλειδιά που δεν υπάρχουν ακόμα.

    #   d = {}
    #   d["apple"].append("fruit")  # ❌ Αυτό θα βγάλει σφάλμα: KeyError

    #   from collections import defaultdict
    #   d = defaultdict(list)
    #   d["apple"].append("fruit")  # ✅ Δεν βγάζει σφάλμα: δημιουργεί κενή λίστα και προσθέτει

    #   Έτσι, δεν χρειάζονται ελέγχοι του τύπου if key not in dict:
    #   dict[key] = []

    #   defaultdict(...): Το όρισμα είναι η default τιμή της συνάρτησης.
    #   defaultdict(list) → κάθε νέο key έχει ως default μια κενή λίστα
    #   defaultdict(dict) → κάθε νέο key έχει ως default ένα κενό λεξικό
    #   defaultdict(lambda: 0) → κάθε νέο key έχει αρχική τιμή 0

    #   geo_hits = defaultdict(lambda: defaultdict(list))
    #   Δημιουργούμε ένα λεξικό geo_hits, όπου κάθε key, δηλαδή κάθε χώρα, οδηγεί σε ένα νέο defaultdict(list). Αυτός o defaultdict περιέχει πεδία και λίστες.

    # Προγραμματιστικά, αυτό μεταφράζεται σε:
#       geo_hits = {
#           "France": {
#               "study_description": ["κείμενο1", "κείμενο2", ...],
#               "study_title": ["άλλο κείμενο"]
#           },
#           "Italy": {
#               "description": ["παράδειγμα που αναφέρει Italy"]
#           },
#           ...
#       }

# geo_hits["Greece"]["study_description"].append("…κείμενο που περιέχει τη λέξη Greece…")


import json
import pycountry
import re
from collections import defaultdict

# Βήμα 2: Φόρτωση JSON αρχείου εισόδου
with open("samples_without_geo.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Βήμα 3: Δημιουργία λίστας με επίσημα ονόματα χωρών. Φτιάχνει ένα σύνολο (set) με όλα τα επίσημα ονόματα χωρών από τη βιβλιοθήκη pycountry.
# pycountry.countries Κάνει loop ένα κατάλογο χωρών. Επιστρέφει μια λίστα από αντικείμενα country, το καθένα περιέχει διάφορα στοιχεία για μια χώρα.
# Για κάθε country μέσα στο pycountry.countries, πάρε το country.name.
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
