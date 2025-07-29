# Βήμα 1: Εισαγωγή βιβλιοθηκών.
import json

# Βήμα 2: Ανάγνωση του αρχείου json_merge, ως μεταβλητή file.
with open("results_merged_json.txt", "r", encoding="utf-8") as file:

    # Bήμα 3: Αποθήκευση τοu αντικείμενου python file μέσω του json.load, μετατροπή σε λίστα python. Ορισμός της λίστας python ως samples.
    samples = json.load(file)

# Βήμα 4: Μέτρηση του συνολικού αριθμού δειγμάτων. Η len μετράει όλα τα αντικείμενα της λίστας python samples και δίνει αριθμιτική τιμη για τα πόσα είναι. Η αριθμιτική αυτή τιμή αποθηκεύεται στην μεταβλητή total_samples.
    total_samples = len(samples)

# Βήμα 5: Ορισμός της λίστας python samples_without_geo, με κάθε αντικείμενό της να είναι τα δείγματα χωρίς την γεωγραφική πληροφορία. Ορίζεται λίστα python samples_without_geo, όπου κάθε αντικείμενο της είναι αντικείμενο της λίστας samples, εφόσον δεν ισχύει για αυτά η συνθήκη. Η συνθήκη είναι η .get() να επιστρέφει πληροφορία country, location_end, location, location_start, isolation_source. Κάθε αντικείμενο των λιστών samples_without_geo και samples ορίζεται ως registry και registry.
samples_without_geo = [
    registry for registry in samples if not (
        registry.get("country") or
        registry.get("location_end") or
        registry.get("location") or
        registry.get("location_start") or
        registry.get("isolation_source")
    )
]

# Βήμα 6: Μέτρηση του συνολικού αριθμού των δειγμάτων χωρίς γεωγραφική πληροφορία μέσω της len.
total_samples_without_geo = len(samples_without_geo)

# Βήμα 7: Εκτύπωση αποτελεσμάτων στην κονσόλα.
print(f"Συνολικός αριθμός δειγμάτων που περιέχονται στο results_merged_json.txt αρχείο : {total_samples}")
print(f"Δείγματα χωρίς καμία γεωγραφική πληροφορία: {total_samples_without_geo}")

# Βήμα 8: Αποθήκευση των δειγμάτων χωρίς γεωγραφική πληροφορία σε νέο αρχείο samples_without_geo.json. Το αρχείο ανοίγεται σε λειτουργία εγγραφής ως μεταβλητη file.
with open("samples_without_geo.json", "w", encoding="utf-8") as file:
    # Μέσω της json.dump, η λίστα python samples_without_geo εγγραφεται στο json αρχείο file, δηλαδή το json αρχείο samples_without_geo.json. Η json.dump χρησιμοποιεί την λίστα python samples_without_geo, για να εγγράψει τη μεταβλητή file, η οποία ορίστηκε πάνω ως το samples_without_geo.json. Εσοχή 2 για ευκολότερη ανάγνωση και όχι σε ειδικούς χαρακτήρες.
    json.dump(samples_without_geo, file, indent=2, ensure_ascii=False)

# Βήμα 9: Ανακοίνωση στην κονσόλα της δημιουργίας json αρχειού που έχει τα δείγματα χωρίς τα γεωγραφικά δεδομένα.
print("Το αρχείο 'samples_without_geo.json' δημιουργήθηκε επιτυχώς!")
