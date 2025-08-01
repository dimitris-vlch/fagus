# Βήμα 1: Εισαγωγή των απαιρήτητων βιβλιοθηκών.
import json
import sys 
# Θα ορίσουμε μια συνάρτηση. Τί είναι μια συνάρτηση python; Είναι ένα μπλοκ κώδικα που μπορούμε να το ανακαλούμε όποτε επιθυμούμε, ώστε να αποφεύγονται οι επαναλήψεις κώδικα. Η λέξη def χρησιμοποείται για να οριστεί μια συνάρτηση. Στην συνέχεια ορίζεται το όνομα της συνάρτησης και μετά μέσα σε παρενθέσεις το όρισμα της συνάρτησης, το οποίο και στην περίπτωση μας θα είναι το όνομα του json αρχείου.
# Bήμα 2: ορίζουμε μια συνάρτηση, που θα μετράει τον αριθμό των δειγμάτων σε ένα αρχείο json. Το όνομα είναι count_samples, είναι περιγραφικό για τη λειτουργία της. Το όρισμα είναι json_file και αναμένεται να είναι το μονοπάτι για ένα αρχείο json, για το οποίο και θα εκτελέσει το κώδικα που βρίσκεται μέσα στο μπλοκ της συνάρτησης. Η συνάρτηση τελείωνει εκεί που σταματά να υπάρχει εσοχή.
def sample_count(json_file):
# Βήμα 3: Έλεγχος οτι το αρχείο json όντως υπάρχει και οτι ο κώδικας του μπλοκ μπορεί να εκτελεστεί κανονικά. Θα επιχειρήσουμε να το καταφέρουμε αυτό μέσω της μεθόδου try-except:
    try:
        # Βήμα 4: Ανάγνωση του αρχειου json, μετατροπή του σε λίστα python μέσω του json.load(file) και αποθήκευση της λίστας σε μεταβλητή data.
        with open(json_file, "r", encoding="utf-8") as file: 
            data = json.load(file)
            # Βήμα 5: Καταμέτρηση των αντικειμένων στην λίστα data και ορισμός του αποτελέσματος στη μεταβλητή sample_count
            sample_count = len(data)
            # Βήμα 6: Εκτύπωση των αποτελεσμάτων της καταμέτρησης των δειγμάτων του json. Αξιοποιείται η μεταβλητή sample_count
            print(f"Ο συνολικός αριθμός των δειγμάτων είναι: {sample_count}")
            if sample_count == 0:
                print("Το αρχείο json δεν περιέχει δείγματα.")
    # Βήμα 7: Μηχανισμός διαχείρισης σφαλμάτων της python κατά την εκτέλεση του κωδικα.Το except καταγραφεί σφάλματα στον κώδικα που υπάγεται η try. Μπορεί να συνοδεύτει από τους όρους FileNotFoundError, JSONDecodeError. Exception as e: το exception είναι κλάση σφαλμάτων που το αποθηκεύει το σφάλμα που παρατηρεί η python στη μεταβλητή e. Το πρόγραμμα δεν σταματά αν υπάρχει σφάλμα, απλώς το καταγράφει.
    except Exception as e:
        # Βήμα 8: Εκτύπωση μυνήματος σφάλματος. Εκτυπώνεται η μεταβλητή e στην οποία και κατεγράφη το σφάλμα. 
            print(f"Σφάλμα κατά την ανάγνωση του αρχείου: {e}")
# Βήμα 10: Ορίζουμε μια νέα συνάρτηση, def count_samples_with_location(json_file): και καταμετρά πόσα εκ των δειγμάτων φέρουν γεωγραφικές συντεταγμένες. Μετράει πόσα dictionary της λίστας data έχουν συμπληρωμένη τη στήλη location. Το όρισμα της συνάρτησης είναι το json_file, που είναι το όνομα του αρχείου json που δίνει ο χρήστης, ενώ το όνομα περιγράφει τη λειτουργία.
def count_samples_with_location(json_file):
    # Βήμα 11: Η συνάρτηση προσπαθεί να αναγνώσει το αρχείο json και να το μετατρέψει σε αντικείμενο python, τη λίστα data.
    try: #sosaki το try και το except πρέπει να έχουν την ίδια εσοχή! 
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Bήμα 12: Ορισμός μεταβλητής count_with_location και εκτύπωση του αποτελέσματος. for sample in data, δηλαδή για κάθε αντικείμενο (sample) στη λίστα (data), αν είναι συμπληρωμένο το πεδίο location του sample (που μεταφράζεται σε sample.get(location)), πρόσθεσε 1 (sum (1)). Δηλαδή κάθε δείγμα που έχει location, και στο json συνοδεύεται πάντα από location start και location end, καταμετράται ως μια μονάδα, και το άθροισμα αυτών ανακοινώνεται στην συνέχεια.
            count_with_location = sum(1 for sample in data if sample.get("location")) 
            print(f"Ο αριθμός των δειγμάτων με γεωγραφικές συντεταγμένες είναι: {count_with_location}")
            if count_with_location == 0:
                print("Δεν υπάρχουν δείγματα που να περιέχουν γεωγραφικές συντεταγμένες.")
            # Βήμα 13: Ορισμός σφάλματος e και εκτύπωσή του μαζί με μύνημα:
    except Exception as e: 
        print(f"Σφάλμα κατά την ανάγνωση του αρχείου: {e}")
#Βήμα 14: Επιθυμούμε να φτιάξουμε μια συνάρτηση που θα μετράει το σύνολο των δειγμάτων που στηρίζονται σε κάποια μελέτη. Ο ποιο εύκολος τρόπος να το πετύχουμε αυτό είναι να μετρήσουμε πόσα εκ των δειγμάτων έχουν συμπληρωμένο το πεδίο study_accession.
def count_samples_with_study(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            count_with_study = sum(1 for sample in data if sample.get("study_accession"))
            print(f"Ο αριθμός των δειγμάτων που στηρίζονται σε μελέτη είναι: {count_with_study}")
            if count_with_study == 0:
                print("Δεν υπάρχουν δείγματα που στηρίζονται πάνω σε μελέτη.")
 
    except Exception as e:
        print(f"Σφάλμα κατά την ανάγνωση του αρχείου: {e}")
# Βήμα 15: Λήψη του ονόματος αρχείου από την γραμμή εντολών. Το όνομα που δίνει ο χρήστης ορίζεται ως η μεταβλητή json_file, η οποία και είναι το όρισμα της συνάρτησης που μετράει τον αριθμό των δειγμάτων. Έτσι, ο χρήστης επιλέγει ποιο θα είναι το αρχείο json για το οποίο τα δείγματα θα μετρηθούν.
json_file = sys.argv[1]
# Bήμα 16: Επιπλέον συνάρτηση για τον υπολογισμό των δειγμάτων που αναφέρεται η χώρα προέλευσης του δείγματος.
def count_samples_with_country(json_file):
    try:
        with open (json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            count_with_country = sum(1 for sample in data if sample.get("country"))
            print(f"Ο αριθμός των δειγμάτων που αναγράφουν χώρα προέλευσης είναι: {count_with_country}")
            # Βήμα 17: Παροχή διευκρίνισης σε περίπτωση που το αρχείο json δεν περιέχει δείγματα με χώρα προέλευσης.
            if count_with_country == 0:
                print("Προσοχή: Δεν υπάρχουν δείγματα με χώρα προέλευσης.")
    except Exception as e:
        print(f"Σφάλμα κατά την ανάγνωση του αρχείου: {e}")
# Βήμα 18: Σε περίπτωση που ο χρήστης δεν ορίσει το json αρχείο στην γραμμή εντολών με τη μορφή python3 json.metrics.py (name.of.the.json.txt), προτείνεται οδηγία, απαιτείται το άθροισμα των ορισμάτων να είναι μεγαλύτερο του 2(το 1ο είναι το json.metrics.py και το δεύτερο name.of.the.json.txt)
if len(sys.argv) < 2:
    print("Try: python3 json.metrics.py name.of.the.json.txt")
    sys.exit(1)
# Βήμα 19: Καλούμε τις συνάρτησεις, προκειμένου να μετρήσουμε τον αριθμό των δειγμάτων, καθώς και τον αριθμό των δειγμάτων που παρουσιάζουν τοποθεσία, και τον αριθμό των δειγμάτων που συνοδεύονται από κάποια μελέτη ή χώρα προέλευσης για τη μεταβλητή json_file.
sample_count(json_file)
count_samples_with_location(json_file)
count_samples_with_study(json_file)
count_samples_with_country(json_file)
