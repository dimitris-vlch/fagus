# Φτιάχνουμε ένα σκριπτάκι που ελέγχει τις γεωγραφικές συντεταγμένες της κάθε καταχώρησης, για το κατα πόσο αντιστοιχούν στην χώρα που έχει δηλωθεί. θεωρείται ότι αρκετές φορές ο ερευνητής κατά την συμπλήρωση των πεδίων των καταχωρήσεων, ενδεχομένως να μπερδέψει το latitude με το lontitude, η να συμπληρώσει την χώρα που εντοπίζεται το ερευνητικό ίδρυμα, αντί της χώρας συλλογής του δείγματος. Αυτοί και άλλοι λόγοι, επισημαίνουν την ανάγκη πραγματοποίησης της διόρθωσης αυτής στα μεταδεδομένα καταχωρήσεων του δείγματος.

# Bήμα 1: Εισαγωγή βιβλιοθηκών. matplotlib για διάγραμμα pie chart.

# Η geopandas μας επιτρέπει να δουλεύουμε με γεωμετρικά αντικείμενα (σημεία, γραμμές, πολύγωνα) μέσα σε dataframe.
# Η βιβλιοθήκη pandas χρησιμοποείται για δεδομένα σε πίνακες και θα φορτώσουμε μέσω αυτής το json αρχείο.
# Η γνωστή pycountry, έχει τα επίσημα ISO codes των χωρών.
# Η βιβλιοθήκη shapely δουλεύει με γεωμετρικά σχήματα. Από αυτή εισάγουμε το αντικείμενο Point. Θα μετατρέψουμε τα lat & lot σε σημεία στο χώρο (γεωμετρικά). Τα οποία θα τα επεξεργαστούμε σε GeoPandas.

import json
import matplotlib.pyplot as plt # type: ignore
import geopandas as gpd
import pandas as pd
import pycountry
from shapely.geometry import Point

# Βήμα 2: Εισαγωγή json αρχείου.

with open ("results_merged_json.txt", "r", encoding= "utf-8") as file:    
    data = json.load(file)

total_registries= len(data)

# Βήμα 3: Αποσπάμε τις εγγραφές που έχουν συμπληρωμένα τα πεδία lat, lon και country ταυτόχρονα, για τον σκοπό  της προκειμένης διεργασίας.
# [entry for entry in data if ...]
# [<τι θα βάλεις στη λίστα> for <κάθε στοιχείο> in <συλλογή> if <κάποια συνθήκη>] 

country_and_coordinates_data = [registry for registry in data if registry.get("lat") and registry.get("lon") and registry.get("country")]
total_geo_registries = len(country_and_coordinates_data)

# δηλαδή για κάθε στοιχείο registry της λίστας data, βάζουμε στοιχείο registry στην λίστα country_and_coordinates_data, εάν ισχύει η συνθήκη if.

# Bήμα 4: Αποθήκεση επιθυμητών εγγραφών σε json.

with open("country_and_coordinates_data.json.txt", "w", encoding="utf-8") as file:
    json.dump(country_and_coordinates_data, file, indent=2, ensure_ascii=False)
    
# Βήμα 5: Ανακοίνωση αποτελεσμάτων στον κένσορα.

print(f"\n\nA total of {total_geo_registries} registries have been found that contain both coordinates and country information, and these have been written in country_and_coordinates_data.json.txt")

# Bήμα 6: Ενα συνοδευτικό pie chart για τα αποτελέσματα με κλεμμένο κώδικα από το προηγούμενο σκριπτ.

no_data = total_registries - total_geo_registries
sizes = [total_geo_registries, no_data]
labels = ["registries with country and coordinates","no data"]
colors = ["blue", "red"]

plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors = ["blue","red"])
plt.title("Ποσοστό δειγμάτων με ή χωρίς γεωγραφική πληροφορία πηγής απομονώσεως")
plt.tight_layout()
plt.savefig("countries_and_coordinates_pie_chart.png")
plt.show()

# Βήμα 7: Επεξεργασία του country_and_coordinates_data.json.txt : αλλαγή της ονομασίας του πεδίου country σε country submitted.

for registry in data:
    registry["country_submitted"] = registry.pop("country", "") # το country φεύγει και μπαίνει country_submitted.

# Bήμα 8: Για κάθε εγγραφή κρατάμε μονάχα τα πεδία lat, lon, country_submiited

# Η στρατιγική μας. Δημιουργούμε μια κενή λίστα country_and_coordinates_data στην οποία στο τέλος θα την γεμίσουμε με .append(geo_registry). Δημιουργούμε το geo_registry μεσα σε μια for με την παραπάνω συνθήκη if για να βάλουμε μονάχα τα κατάλληλα δείγματα. Στην συνέχεια φτιάχνουμε geo_registry = {"πεδιο" registry.get("πεδιο")}   

country_and_coordinates_data = []

for idx, registry in enumerate(data,1): # τροποποιούμε λιγο το for registry in data: για να χουμε καταμέτρηση δειγμάτων με idx & enumarate
    if registry.get("lat") and registry.get("lon") and registry.get("country_submitted"):
        geo_registry = {
            "Registry number:" : idx,         
            "sample_accession" : registry["sample_accession"],
            "lat" : registry["lat"],
            "lon" : registry["lon"],
            "country_submitted" : registry["country_submitted"]
        }
        country_and_coordinates_data.append(geo_registry)

# Βήμα 9: Παρασκευή json αρχείου που περιέχει μόνο τα δεδομένα που μας ενδιαφέρουν.

with open("country_and_coordinates_minimal_data.json.txt", "w", encoding = "utf-8") as file:
    json.dump(country_and_coordinates_data, file, indent = 2, ensure_ascii= False )

# Aνακοίνωση αποτελεσμάτων στον κένσορα:

print (f"\ncountry_and_coordinates_minimal_data.json.txt has been created successfully. This json file contains {len(country_and_coordinates_data)} registries with both country and coordinates and only these fields from the whole registry, as well as the sample_accession field for identification\n")

# Βήμα 10: Έλεγχος της εγκυρότητας των γεωγραφικών δεδομένων μέσω της βιβλιοθήκης geo_pandas

# Ορισμός dataframe