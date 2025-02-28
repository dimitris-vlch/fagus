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
