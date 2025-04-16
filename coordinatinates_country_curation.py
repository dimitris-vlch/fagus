# Φτιάχνουμε ένα σκριπτάκι που ελέγχει τις γεωγραφικές συντεταγμένες της κάθε καταχώρησης, για το κατα πόσο αντιστοιχούν στην χώρα που έχει δηλωθεί. θεωρείται ότι αρκετές φορές ο ερευνητής κατά την συμπλήρωση των πεδίων των καταχωρήσεων, ενδεχομένως να μπερδέψει το latitude με το lontitude, η να συμπληρώσει την χώρα που εντοπίζεται το ερευνητικό ίδρυμα, αντί της χώρας συλλογής του δείγματος. Αυτοί και άλλοι λόγοι, επισημαίνουν την ανάγκη πραγματοποίησης της διόρθωσης αυτής στα μεταδεδομένα καταχωρήσεων του δείγματος.

# Bήμα 1: Εισαγωγή βιβλιοθηκών. matplotlib για διάγραμμα pie chart.

import json
import matplotlib as plt

# Βήμα 2: Εισαγωγή json αρχείου.

with open ("results_merged_json.txt", "r", encoding= "utf-8") as file:    
    data = json.load(file)

total_samples= len(data)

# Βήμα 3: Αποσπάμε τις εγγραφές που έχουν συμπληρωμένα τα πεδία lat, lon και country ταυτόχρονα, για τον σκοπό  της προκειμένης διεργασίας.
# [entry for entry in data if ...]
# [<τι θα βάλεις στη λίστα> for <κάθε στοιχείο> in <συλλογή> if <κάποια συνθήκη>] 

country_and_coordinates_data = [registry for registry in data if registry.get("lat") and registry.get("lon") and registry.get("country")]

# δηλαδή για κάθε στοιχείο registry της λίστας data, βάζουμε στοιχείο registry στην λίστα country_and_coordinates_data, εάν ισχύει η συνθήκη if.

# Bήμα 4: Αποθήκεση επιθυμητών εγγραφών σε json.

with open("country_and_coordinates_data.json.txt", "w", encoding="utf-8") as file:
    json.dump(country_and_coordinates_data, file, indent=2, ensure_ascii=False)
    
# Βήμα 5: Ανακοίνωση αποτελεσμάτων στον κένσορα.

total_geo_samples = len(country_and_coordinates_data)
print(f"A total of {total_geo_samples} registries have been found that contain both coordinates and country information, and these have been written in country_and_coordinates_data.json.txt")

# Bήμα 6: Ενα συνοδευτικό pie chart για τα αποτελέσματα με κλεμμένο κώδικα από το προηγούμενο σκριπτ.


