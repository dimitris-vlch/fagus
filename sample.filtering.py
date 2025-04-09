#Στόχος είναι να φτιάξουμε ένα δεύτερο σκριπτ για το φιλτράρισμα των μεταδεδομένων από την ΈΝΑ, μα παρόμοιες ιδιότητες όσο είναι δυνατόν με το ομόλογο του σε javascript.
#Βήμα 1: Είσαγωγή βιβλιοθηκών:
#Το πρώτο βήμα είναι να εισάγουμε όλες τις απαραίτητες βιβλιοθήκες που θα χρειαστούμε για να τρέχει το script. Εδώ εισάγουμε τη βιβλιοθήκη json που κωδικοποιεί και αποκωδικοποιεί αρχεία json. Είναι ενσωματομένη στη python και δεν χρειάζεται να την κατεβάσουμε.
#import json
#Βήμα 2: Ανάγνωση του αρχείου json:
#with open("results_sample_json.txt", "r", encoding="utf-8") as file:
#Λέω στην python οτι κάθε στοιχείο {…} του json αντιστοιχεί σε ένα sample.
#samples = json.load(file)
#with: Εξασφαλίζει ότι το αρχείο θα κλείσει σωστά μετά την ανάγνωση.
#json.load(file): Φορτώνει τα δεδομένα JSON από το αρχείο και τα μετατρέπει σε αντικείμενο Python (συνήθως λίστα ή λεξικό).
#samples: Μια λίστα που περιέχει όλα τα δείγματα από το αρχείο.
#Είναι σημαντικό πρώτα να φορτωθούν τα δεδομένα του json σε αντικείμενο Python έτσι ώστε να οριστεί το file. Τότε το json.load(file) έχει οριστεί και μπορεί να διαβάσει τη μεταβλητή samples.
#Βήμα 3: Μέτρηση του συνολικού αριθμού δειγμάτων:
#total_samples = len(samples)
#len(samples): Επιστρέφει τον αριθμό των στοιχείων στη λίστα samples, δηλαδή τον συνολικό αριθμό δειγμάτων. 
#Bήμα 4: Το πιο σημαντικό βήμα: Φιλτράρισμα των δειγμάτων χωρίς γεωγραφικές πληροφορίες:
#filtered_samples = [
#    sample for sample in samples
#    if not (
#        sample.get("country") == "" and
#        sample.get("location_end") == "" and
#        sample.get("location") == "" and
#        sample.get("location_start") == "" and
#        sample.get("isolation_source") == ""
#    )
#]
#Ορίζουμε τα φιλτραρισμένα δείγματα ως τη λίστα filtered_samples. Πρόκειται για λίστα του τύπου list comprehension. new_list = [expression for item in iterable if condition]
#expression → Αυτό που θα προστεθεί στη νέα λίστα. Αναφερόμαστε στα samples.
#item → Το κάθε στοιχείο της λίστας που διατρέχουμε.  Ελέγχει ένα ένα τα samples.
#iterable → Η αρχική λίστα από την οποία παίρνουμε τα στοιχεία. Στο παράδειγμά μας, ορίστηκε στο βήμα 2 αυτη η λίστα ως ένα αντικείμενο της python με όλα τα στοιχεία του json.
#if condition → Μια συνθήκη που καθορίζει ποια στοιχεία θα συμπεριληφθούν. H συνθήκη που ελέγχεται.
#Χρησιμοποιούμε sample.get("key"), γιατί αν το πεδίο λείπει, η .get() επιστρέφει None αντί για σφάλμα.
#Το not  αντιστρέφει τη συνθήκη.
#Αν όλα τα πεδία είναι κενά, τότε το δείγμα θεωρείται άχρηστο και δεν θα συμπερηλιφθεί στο νέο πίνακα filtered.samples.
#Βήμα 5: Υπολογισμός του αριθμού των αφαιρεθέντων δειγμάτων:
#removed_samples = total_samples – len(filtered_samples)
#Πολύ self explanitory βήμα. Σημειώνεται οτι ορίσαμε παραπάνω total_samples = len(samples)
#δλδ πρακτικά removed_samples=  len(samples) – len(filtered_samples).
#Βήμα 6: Εμφάνιση των αποτελεσμάτων:
#print(f"Συνολικός αριθμός δειγμάτων: {total_samples}")
#print(f"Αφαιρέθηκαν {removed_samples} δείγματα χωρίς γεωγραφικές πληροφορίες.")
#print(f"Παραμένουν {len(filtered_samples)} δείγματα.")
#Πολύ self-explanatory βήμα, στη printf {…} για να εκτυπώσει την τιμή μιας μεταβλητής.
#Βήμα 7: Αποθήκευση των φιλτραρισμένων δειγμάτων σε νέο αρχείο JSON:
#with open("results_sample_json_filtered.json", "w", encoding="utf-8") as file:
#    json.dump(filtered_samples, file, indent=2, ensure_ascii=False)
#Ορίζεται το όνομα του νέου αρχείου .json results_sample_json_filtered.json το οποίο και το θέτει σε λειτουργία εγγραφής «w» ενώ το encoding="utf-8" είναι τυπικό.
#Με το with, το αρχείο κλείνει αυτόματα μετά την ολοκλήρωση της εγγραφής.
#json.dump(filtered_samples, file, indent=2, ensure_ascii=False)
#filtered_samples → το νέο json περιέχει τη λίστα filtered samples.
#file → για να κάνει write το αρχείο
#indent=2 → εισάγει δύο εσοχές στο json(ευκολότερη ανάγνωση).
#ensure_ascii=False → τυπικό, για ειδικούς χαρακτήρες.
#Σοσάκι json.dump() → μετατρέπει ένα αντικείμενο python σε json αρχείο.


import json

# Βήμα 1: Ανάγνωση του αρχείου JSON
with open("results_sample_json.txt", "r", encoding="utf-8") as file:
    samples = json.load(file)

# Βήμα 2: Μέτρηση του συνολικού αριθμού δειγμάτων
total_samples = len(samples)

# Βήμα 3: Φιλτράρισμα των δειγμάτων χωρίς γεωγραφικές πληροφορίες
filtered_samples = [
    sample for sample in samples if not (
        sample.get("country") == "" and
        sample.get("location_end") == "" and
        sample.get("location") == "" and
        sample.get("location_start") == "" and
        sample.get("isolation_source") == ""
    )
]

# Υπολογισμός αφαιρεθέντων δειγμάτων
removed_samples = total_samples - len(filtered_samples)

# Βήμα 4: Εμφάνιση των αποτελεσμάτων
print(f"Συνολικός αριθμός δειγμάτων: {total_samples}")
print(f"Αφαιρέθηκαν {removed_samples} δείγματα χωρίς γεωγραφικές πληροφορίες.")
print(f"Παραμένουν {len(filtered_samples)} δείγματα.")

# Βήμα 5: Αποθήκευση των φιλτραρισμένων δειγμάτων σε νέο αρχείο JSON
with open("results_sample_json_filtered.json", "w", encoding="utf-8") as file:
    json.dump(filtered_samples, file, indent=2, ensure_ascii=False)

print("Το νέο αρχείο 'results_sample_json_filtered.json' δημιουργήθηκε επιτυχώς!")
