#   Έχουμε δύο json αρχεία, results_sample_json.txt results_study_json.txt . Καθένα εκ των οποίων προέκυψε από το advanced search της ΕΝΑ και φέρει διαφορετικές χρήσιμες πληροφορίες για δείγματα του των ειδών του γένους fagus. Ενδιαφερόμαστε να πάρουμε ορισμένες πληροφορίες απο το results_study_json.txt και να τις ενσωματώσουμε στο αρχείο results_sample_json.txt. Σκοπεύουμε να αξιοποιήσουμε το μοναδικό κωδικό για κάθε μελέτη study_accession, προκειμένου να συνδιάσουμε σωστά τις πληροφορίες των 2 json. Μια μελέτη αντιστοιχεί σε μια μοναδική ομάδα δειγμάτων, και κάθε δείγμα αναγράφει το study_accession της μελέτης που αυτό ανήκει. Έτσι, ο συνδιασμός των δυο αρχείων json είναι εφικτός.
#   Πρακτικά μιλώντας, σκοπός είναι να έχουμε ένα json αρχείο, που θα περιλαμβάνει επιπλέον χρήσιμες πληροφορίες, η οποίες δεν υπάρχουν εξαρχής στο results_sample_json.txt με το οποίο και έχουμε εργαστεί μέχρι στιγμής. Στην συνέχεια, μπορούμε να συνεχίσουμε το workflow κανονικά, απλά με το νέο εμπλουτισμένο json αρχείο.
#   Ενότητες που θα προσθέσουμε στο json αρχείο, από το results_study_json.txt, είναι study_title, description, study_description, καθώς αυτές είναι που περιέχουν χρήσιμες πληροφορίες για τα δείγματα.
# Ακολουθεί το σκριπτ που θα ενσωματώνει τα δεδομένα των 2 json αρχείων.

# Bήμα 1: Θα ορίσουμε μια συνάρτηση η οποία θα είναι υπεύθυνη για την συναρμολόγηση του νέου json αρχείου. Την ονομάζουμε merge_json_by_study_accession, έχει ως ορίσματα 3 json αρχεία, το results_study_json.txt, το results_sample_json.txt και το output json αρχείο, που μπορούμε να το ονομάσουμε results_merged_json.txt. Στην συνέχεια την καλούμε ώστε να εκτελέσει την συγχώνευση των αρχείων.
    # Βήμα 2: Εισαγωγή βιβλιοθηκών, ανάγνωση json αρχείων που θα αξιοποιήσουμε, μετατροπή αυτών σε αντικείμενα python και αποθήκευση αυτών σε μεταβλητές.

import json  # ΣΟΣ στα ονόματα των αρχείων, όχι τελείες!

def merge_json_by_study_accession(sample_json, study_json, merged_json): 
    # Βήμα 1: Εισαγωγή βιβλιοθηκών, ανάγνωση json αρχείων που θα αξιοποιήσουμε, μετατροπή αυτών σε αντικείμενα python και αποθήκευση αυτών σε μεταβλητές.
    with open(study_json, "r", encoding="utf-8") as file:
        data_study = json.load(file)
    
    with open(sample_json, "r", encoding="utf-8") as file:
        data_sample = json.load(file)

    # Βήμα 2: Ορίζουμε μια λίστα-αντικείμενο python, την μεταβλητή data_to_merge η οποία και θα περιέχει όλες τις πληροφορίες που επιθυμούμε να ενσωματώσουμε στο script.
    # Χρησιμοποιούμε ως κλειδί το study_accession για κάθε στοιχείο (study) στη λίστα και μέσω της .get(), εξάγουμε από κάθε στοιχείο της λίστας data_study
    # τα study_title, description, study_description. Πλέον αυτά ανήκουν στην μεταβλητή data_to_merge.
    data_to_merge = {
        study["study_accession"]: {  
            "study_title": study.get("study_title", ""),  
            "description": study.get("description", ""),  
            "study_description": study.get("study_description", "")  
        }
        for study in data_study  # H for study in data_study διαβάζει ένα ένα κάθε στοιχείο (study) της λίστας data_study, που περιέχει όλα τα δεδομένα του study_json.
    }

    # Βήμα 3: Συγχώνευση της λίστας data_sample με την λίστα data_to_merge, αξιοποιώντας το study_accession.
    # Το πιο σημαντικό βήμα του script. Δεν δημιουργούμε μια νέα λίστα, αλλά ενημερώνουμε τα δεδομένα που υπάρχουν στην data_to_merge.
    for sample in data_sample:
        # Ορίζουμε μια υπολίστα study_accession της λίστας sample_data, και κάθε στοιχείο της είναι απλώς το sample_accession,
        # που το βρίσκει η .get() από τη μεγάλη λίστα data_sample. Η νέα λίστα sample_accession θα είναι ο συνδετικός μας κρίκος για το νέο json που θα προκύψει.
        study_accession = sample.get("study_accession", "")

        # SOS: Εάν η λίστα ΠΟΥ ΠΡΟΚΥΠΤΕΙ ΑΠΟ ΤΟ sample_data ΕΜΠΕΡΙΕΧΕΤΑΙ ΣΤΗ data_to_merge !!! Τότε:
        if study_accession in data_to_merge:
            # Ενημέρωσε κάθε αντικείμενο της λίστας sample_accession, με τα περιεχόμενα της data_to_merge.
            # Πλέον, η sample_accession περιέχει τα δεδομένα της data_to_merge και συνεπώς η data_sample περιέχει όλα τα επιθυμητά δεδομένα που χρειαζόμαστε.
            # Αρκεί τώρα να τα εκτυπώσουμε στο νέο json αρχείο.
            sample.update(data_to_merge[study_accession])

    # Βήμα 4: Δημιουργία του json.merged αρχείου σε λειτουργία εγγραφής.
    with open(merged_json, "w", encoding="utf-8") as file:
        # Βήμα 5: Εγγραφή του merged.json αξιοποιώντας την json.dump().
        # Το json.dump() χρησιμοποιεί τα δεδομένα της συγχωνεμένης λίστας data_sample, ως φάκελος file, με ensure_ascii=False για ελληνικούς χαρακτήρες
        # και αφήνει και επιπλέον εσοχή 4 ώστε το json αρχείο να είναι περισσότερο εμφανίσιμο.
        json.dump(data_sample, file, ensure_ascii=False, indent=4)

    # Βήμα 6: Ανακοίνωση ολοκλήρωσης της διεργασίας.
    print(f"Created {merged_json}.")
    print(f"{merged_json} contains important additional data, such as description, study description, and study title.")

# Βήμα 7: Ορισμός των ονομάτων των json αρχείων που αξιοποιούνται και απορρέουν από το script.
sample_json = "results_sample_json.txt"
study_json = "results_study_json.txt"
merged_json = "results_merged_json.txt"

# Βήμα 8: Ανάκληση της συνάρτησης:
# Δεν βάζουμε .txt απευθείας στην συνάρτηση, για αυτό και ορίσαμε τα ονόματα των αρχείων ως μεταβλητές παραπάνω.
merge_json_by_study_accession(sample_json, study_json, merged_json)
