# Βήμα 1: Εισαγωγή βιβλιοθηκών json και csv.
# Η βιβλιοθήκη json χρησιμοποιείται για την επεξεργασία json αρχείων και η βιβλιοθήκη csv χρησιμοποιείται για την εγγραφή δεδομένων σε csv.  
import json
import csv
# Βήμα 2: Ορίζουμε μεταβλητές για τα αρχεία json και csv ώστε να είναι το script περισσότερο ευανάγνωστο:
json_file = "results_sample_json.txt"
csv_file  = "results_sample.csv"
# Βήμα 3:  Άνοιγμα και ανάγνωση json αρχείου.
# Ανοίγουμε το αρχείο results_sample_json.txt, σε λειτουργία ανάγνωσης “r” και για ειδικούς χαρακτήρες utf-8.
# Ορίζοντας τώρα το file, ως json.load(file), το μετατρέπουμε σε python αντικείμενο, μιά λίστα την οποία και στην συνέχεια την ορίζομουμε ως data.
with open(json_file, "r", encoding="utf-8") as file:
    data = json.load(file)
# Bήμα 4: Άνοιγμα και write για το αρχείο csv.
# Θα δημιουργήσει αρχείο  results_sample_json.csv, σε λειτουργία εγγραφής “w”, που δέχεται ειδικούς  χαρακτήρες encoding="utf-8". To newline="" αποτρέπει
# την εισαγωγή κενών γραμμών.
with open(csv_file, "w", encoding="utf-8", newline="") as file:
# Βήμα 5: έλεγχος αν το αρχείο json περιέχει δεδομένα. Το βήμα αυτό δεν είναι απαραίτητο, το χρησιμοποιύμε αν θέλουμε να αποτρέψουμε την δημιουργία κενών αρχείων csv,
# από λήψεις κενών json αρχείων. Σε περίπτωση που το Json είναι άδειο (if not data:) τότε θα σταματήσει το script sys.exit(1), αφού θα εκτυπώσει το μύνημα με print.
    if not data: 
        print("Το JSON αρχείο είναι κενό. Διακοπή μετατροπής.")
        sys.exit(1)
        # Βήμα 5: Προετοιμασία του αρχείου csv
        # 5.1: Η μέθοδος .keys() επιστρέφει όλα τα κλειδιά (keys) από το dictionary. Δηλαδή για την περίπτωσή μας επιστρέφει "sample_accession", "country", "location"
        # και συγκεκριμένα παίρνει από το πρώτο dictionary της λίστας data[0].keys(). Η νέα λίστα που δημιουργείται ορίζεται ως fieldnames.
    fieldnames = data[0].keys()
    # 5.2: Δημιουργούμε έναν writer για το csv. Με το csv.DictWriter εγγράφουμε τα δεδομένα στο csv. Μας ενδιαφέρει πρώτα να ενσωματώσουμε τα περιεχόμενα της
    # data[0].keys(), τα οποία και είναι δλδ τα "sample_accession", "country", "location" κλπ. Με το file εξηγούμε ποιο είναι το csv που αναφερόμαστε που θα χρησιμοποιήσει
    # writer. Ο πρότος όρος fieldnames αναφέρετε στα δεδομένα ("sample_accession", "country", "location") και το fieldnames=fieldnames εξηγεί στο writer οτι πρέπει
    # να τα γράψει στο csv όπως έχουν.
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    # 5.3: με το writerheader εξηγούμε οτι τα παραπάνω είναι η πρώτη γραμμή του csv.
    writer.writeheader()
    # 5.4: Συμπλήρωση από της επόμενης (2ης) μέχρι και της τελευταίας στήλης του csv. Το row αναφέρεται σε κάθε dictionary της λίστας ένα ένα ένα με τη σειρά, συγκεκριμένα
    # της λίστας data. Η writerow δεν πειράζει την πρώτη γραμμή γιατί πριν χρησιμοποιήσαμε τη writeheader και αξιοποιεί την write οπως την ορίσαμε παραπάνω. Γράφει κάθε
    # στήλη του csv με τη σειρά, αξιοποιώντας τα dictionary που της παρουσιάζει η row.
    for row in data:
        writer.writerow(row)
    # Βήμα 6: Ανακοίνωση ολοκλήρωσης της διεργασίας.
    print(f"Η μετατροπή του {json_file} ολοκληρώθηκε! Το αρχείο {csv_file} είναι έτοιμο.")
    