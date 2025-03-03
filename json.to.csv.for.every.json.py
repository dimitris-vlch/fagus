import json
import csv
import sys

# Έλεγχος αν έχουν δοθεί ορίσματα για το αρχείο JSON και το αρχείο CSV
if len(sys.argv) != 3:
    print("Χρήση: python json_to_csv.py <εισ_αρχείο.json> <εξ_αρχείο.csv>")
    sys.exit(1)

# Λήψη ονομάτων αρχείων από τα ορίσματα
json_file = sys.argv[1]
csv_file = sys.argv[2]

# Άνοιγμα και ανάγνωση του JSON αρχείου
with open(json_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Άνοιγμα του CSV αρχείου για εγγραφή
with open(csv_file, "w", encoding="utf-8", newline="") as file:
    # Έλεγχος αν υπάρχουν δεδομένα στο JSON
    if len(data) > 0:
        # Ορισμός των πεδίων (στηλών του CSV)
        fieldnames = data[0].keys()
        
        # Δημιουργία του CSV writer και εγγραφή της κεφαλίδας
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # Εγγραφή των δεδομένων στο CSV
        for row in data:
            writer.writerow(row)

print(f"Η μετατροπή του '{json_file}' σε CSV ολοκληρώθηκε! Το αρχείο '{csv_file}' είναι έτοιμο.")
