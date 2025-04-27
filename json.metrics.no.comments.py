import json
import sys 

def sample_count(json_file):
    try:c
        with open(json_file, "r", encoding="utf-8") as file: 
            data = json.load(file)
            sample_count = len(data)
            print(f"Ο συνολικός αριθμός των δειγμάτων είναι: {sample_count}")
            if sample_count == 0:
                print("Το αρχείο json δεν περιέχει δείγματα.")
    except Exception as e:
            print(f"Σφάλμα κατά την ανάγνωση του αρχείου: {e}")

def count_samples_with_location(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            count_with_location = sum(1 for sample in data if sample.get("location")) 
            print(f"Ο αριθμός των δειγμάτων με γεωγραφικές συντεταγμένες είναι: {count_with_location}")
            if count_with_location == 0:
                print("Δεν υπάρχουν δείγματα που να περιέχουν γεωγραφικές συντεταγμένες.")
    except Exception as e: 
        print(f"Σφάλμα κατά την ανάγνωση του αρχείου: {e}")

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
json_file = sys.argv[1]

def count_samples_with_country(json_file):
    try:
        with open (json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            count_with_country = sum(1 for sample in data if sample.get("country"))
            print(f"Ο αριθμός των δειγμάτων που αναγράφουν χώρα προέλευσης είναι: {count_with_country}")
            if count_with_country == 0:
                print("Προσοχή: Δεν υπάρχουν δείγματα με χώρα προέλευσης.")
    except Exception as e:
        print(f"Σφάλμα κατά την ανάγνωση του αρχείου: {e}")
if len(sys.argv) < 2:
    print("Try: python3 json.metrics.py name.of.the.json.txt")
    sys.exit(1)

sample_count(json_file)
count_samples_with_location(json_file)
count_samples_with_study(json_file)
count_samples_with_country(json_file)
