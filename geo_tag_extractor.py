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

# Βήμα 2: Φόρτωση JSON αρχείου εισόδου και μετατροπή του σε λεξικό python.
with open("samples_without_geo.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Βήμα 3: Δημιουργία λίστας με επίσημα ονόματα χωρών. Φτιάχνει ένα σύνολο (set) με όλα τα επίσημα ονόματα χωρών από τη βιβλιοθήκη pycountry.
# pycountry.countries Κάνει loop ένα κατάλογο χωρών. Επιστρέφει μια λίστα από αντικείμενα country, το καθένα περιέχει διάφορα στοιχεία για μια χώρα.
# Για κάθε country μέσα στο pycountry.countries, πάρε το country.name.

country_names = set(country.name for country in pycountry.countries)

# Βήμα 4: Regex pattern με όλες τις χώρες. Φτιάχνει ένα regex pattern.
# re.compile : δημιουργεί regex αντικείμενο με το οποίο και κάνουμε αναζήτηση.

# pattern_string = r'\b(' + '|'.join(re.escape(name) for name in sorted(country_names, key=len, reverse=True)) + r')\b'

#   r'\b('  ==> κανόνας regex που λέει από την αρχή μια λέξεις κάνε τα παρακάτω:
#        r'...' για raw string, η python δεν ερμηνεύει backslashes (τενχικό κυρίως)
#        \b regex συμβολο που δηλώνει αρχή και τέλος λέξης.
#        ( ανοίγει ένα capturing group, μια ομάδα δηλάδη επιλογών.

#   '|'.join(...) ==> δημιουργεί μια λίστα με τα ονόματα των χωρών χωρισμένα. το | σημαίνει ή διαζευτικό

#   re.escape(name) for name in τυπικό βήμα, για κάθε όνομα φροντίζει οι ειδικοί χαρακτήρες να ενσωματοθούν σωστά.

#   sorted(country_names, key=len, reverse=True)
    # ταξινόμιση ονομάτων χώρας (country_names), κατα φθίνουσα σειρά (key=len, reverse=True). Έτσι το "United States of America" δεν θα ταιριάξει στο America.

#   + r')\b' ==> κλείνουμε το capturing group, και βάζουμε όριο λέξης για κλείσιμο.

# re.IGNORECASE τυπικό βήμα, για να μην είναι case sensitive.

country_pattern = re.compile(
    r'\b(?:' + '|'.join(re.escape(name) for name in sorted(country_names, key=len, reverse=True)) + r')\b',
    re.IGNORECASE
)

# Βήμα 5: Ανίχνευση χωρών σε όλα τα πεδία κάθε εγγραφής.

# for registry in data: Για κάθε εγγραφή του samples_without_geo.json
# for field, value in registry.items(): Για το περιεχόμενο (value) του κάθε αντικειμένου (field) της κάθε εγγραφής registry.item() τις εγγραφές τις διατρέχουμε μία-μία.
# if isinstance(value, str) and value.strip(): τυπικός έλεγχος ελέγχουμε οτι το το αντικείμενο value, του λεξικού registry, οτι είναι τύπου str και όχι κενό, white space.
# matches = country_pattern.findall(value) για το value, που είναι κάθε εγγραφή και αντικείμενο της καθε πεδίο (field), εφαρμόζουμε το regex country_pattern για να δούμε σε πόσα πεδία κάθε εγγραφής (value) βρέθηκε το country_pattern. Δηλαδή, για κάθε εγγραφή επιστρέφουμε μια λίστα με όλες τις λέξεις που αναγνωρίστηκαν ως χώρες.
# for match in matches: για κάθε λέξη που εντοπίστηκε ως χώρα στη λίστα με τις χώρες που εντοπίστηκαν για ενα πεδίο(field):
# match_clean = match.strip() καθαρίζουμε τυχόν κενά για λόγους συνέπειας.




geo_hits = defaultdict(lambda: defaultdict(list))

for registry in data:
    for field, value in registry.items():
        if isinstance(value, str) and value.strip():
            matches = country_pattern.findall(value)
            for match in matches:
                match_clean = match.strip()

# Βήμα 6: Αποθήκευση αποτελεσμάτων

# Δημιουργούμε την κενή λίστα results, που αποθηκεύουμε σε αυτήν όλες τις πληροφορίες που επιθυμούμε, τις οποίες και στην συνέχεια θα αποθηκεύσουμε στο json αρχείο.

# for country, field_map in geo_hits.items() Για κάθε χώρα, παίρνουμε τον εσωτερικό χάρτη πεδίων field_map. country = "France", field_map = {"study_title": [...], "study_description": [...]}

# for field, examples in field_map.items() Διατρέχουμε κάθε πεδίο που περιέχει αποσπάσματα. field = "study_title", examples = ["France is beautiful", "..."]

# Σε αυτή τη χρήση, το .items() μας επιτρέπει να ελένξουμε τι συμβαίνει χώρα προς χώρα.

# H .append() παίρνει τα πεδία που διατρέχουμε (χώρα, πεδίο, λίστα παραδειγμάτων). Και τα προσθέτει στη λίστα results.

results = []

for country, field_map in geo_hits.items():
    for field, examples in field_map.items():
        results.append({
            "country": country,
            "field": field,
            "examples": examples
        })

# Βήμα 7: Εγγραφή σε json και εκτύπωση των αποτελεσμάτων στην κονσόλα.
with open("detected_country_keywords.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=2, ensure_ascii=False)

print(" 'detected_country_keywords.json' was created successfully.")
