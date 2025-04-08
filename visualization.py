# Σκριπτάκι για την γραφική αναπαράσταση των αποτελεσμάτων σε Bar και Pie chart

# Βήμα 1: Εισαγωγή βιλβιοθηκών και ανάγνωση του αρχείου json, μετατροπή του σε λεξικό python.
# Αξιοποιούμε το υποπακέτο pyplot της βιβλιοθήκης matplotlib. Το plt ειναι alias για matplotlib.pyplot. Το pyplot έχει συναρτήσεις για γραφικά διαγράμματα, bar chart, pie charts, συναρτήσεις για τίτλους και ετικέτες, καθώς και για να εμφανίσεις τα διαγράμματα.
# Εισάγουμε την υποβιβλιοθήκη Counter από την βιβλιοθήκη collections. Το Counter το αξιοποιούμε για να δούμε πόσες φορές εμφανίζεται κάθε τιμή. Μας είναι χρήσιμο επειδή έχουμε πολλά δείγματα και κάθε δείγμα έχει διαφορετικά μεταδεδομένα γεωγραφίας, βλέπουμε απλώς την συχνότητα εμφάνισης της τοποθεσίας, της χώρας κλπ.

import json
import matplotlib.pyplot as plt
from collections import Counter 

with open("results_merged_json.txt", "r", encoding="utf-8") as file:
    data = json.load(file)

# Βήμα 2: Ορίζουμε ένα λεξικό, geo_data, οπου κάθε αντικείμενό του είναι ένα πεδίο των αντικειμένων του λεξικού data, το οποίο και όμως φέρει γεωγραφική πληροφορία. Πεδιά του στύλ χώρα, συντεταγμένες lat, lon, κλπ.

geo_fields = [
    "country", "location", "location_start", "location_end", "isolation_source", "lat", "lon"
]

# Βήμα 3: Ορίζουμε τις μεταβλητές που θα χρειαστούμε για την καταμέτρηση. Μεταβλητή with_geo και μεταβλητή without_geo που ορίζονται ως μηδεν, καθώς και μεταβλητή που ορίζεται ως κενή λίστα Counter για να εκτελέσει την καταμέτρηση των αντικειμένων σε λεξικό data.

with_geo = 0
without_geo = 0
frequency = Counter()

# Βήμα 4: Ορίζουμε μεταβλητή registry για κάθε αντικείμενο της λίστας data.
# Για κάθε registry στη λίστα data.
    #  Για κάθε registry στη λίστα data, oρίζουμε μια μεταβλητή hits = False, την οποία και θα κάνουμε σωστή, εαν η εγγραφή περιέχει γεωγραφικό δείγμα
    # Ορίζουμε μεταβλητή geo_field για κάθε πεδίο της λίστας geo_fields που φτιάξαμε.
    # Για κάθε πεδίο (geo_field) της λίστας geo_fields:
    # Ελέγχουμε με .get() σε κάθε registry αν επιστρέφονται τιμή για fields ή εαν επιστρέφεται  "", δηλαδή κενό field.
    #registry.get(geo_field, ""). «Δώσε μου την τιμή για το key field από το λεξικό registry. Αν δεν υπάρχει, δώσε μου κενό string 
    # ("") αντί για σφάλμα.»
    # .strip() αφαιρεί κενά, tabs, newlines από την αρχή και το τέλος της τιμής. Έτσι, δεν θα μετρήσουμε ένα κενό ως έγκυρη τιμή.  
    # Έτσι, η value είναι μια καθαρή γεωγραφική τιμή πχ Greece.
    # Aν η .get() επιστρέφει field, τότε ή hits γίνεται αληθής και ο μετρητής για τα πεδία με την γεωγραφική πληροφορία αυξάνεται κατά ένα.
    # Έτσι, η value είτε παίρνει μια καθαρή γεωγραφική τιμή, είτε ένα κενό string.
    # Εαν η value έχει γεωγραφική τιμή και δεν είναι δηλαδή κενό string,    
    # Εαν η hits είναι αληθής, τότε η with_geo αυξάνεται κατά 1, διαφορετικά η without_geo αυξάνεται κατά μια μονάδα.
    # frequency[geo_field] += 1 Κάθε φορά που εμφανίζεται κάποιο geo_field του geo_fields, αυξάνεται η τιμή του geo_field με το counter κατα μια μονάδα.


for registry in data
    hits = False
    for geo_field in geo_fields 
        value = registry.get(geo_field, "").strip()
        if value:
            hits = True
            frequency[geo_field] += 1 

        if hits:
            with_geo =+ 1
        else:
            without_geo =+ 1

# Βήμα 5: Εκτύπωση των αποτελεσμάτων της καταμέτρησης
# for geo_field, count in frequency.items(): Eκτελούμε βρόγχο loop στο αντικείμενο frequency, το οποίο και είναι τύπου Counter.
# .items() Σε λεξικά και σε μεταβλητές τύπου Counter, επιστρέφει σε ζευγάρια (key,value). Έτσι, αφου ολοκληρώθηκε το βήμα 4, θα ισχύει frequency = Counter({ "country": 4435, "lat": 853, "lon": 853, "location": 200 }).
# Δηλαδή θα ισχύει for geo_field, count in frequency.items(): geo_field = "country", count = 4435 geo_field = "lat", count = 853 geo_field = "lon", count = 853 geo_field = "location", count = 200
# geo_field → είναι το όνομα του πεδίου (string)
# count → είναι το πλήθος εμφανίσεων του πεδίου (ακέραιος αριθμός)
# εκτυπώνουμε στην συνέχεια κάθε πεδίο geo_field, συνοδευόμενο από τον ακέραιο αριθμό του count που μετρήσαμε με τη             frequency[geo_field] += 1 

for geo_field, count in frequency.items():
    print(f"{geo_field}: {count}")