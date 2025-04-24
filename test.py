import json
import matplotlib.pyplot as plt 
import geopandas as gpd 
import pandas as pd 
from shapely.geometry import Point 
from geopy.geocoders import Nominatim  

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

print(f"\n\nA total of {total_geo_registries} registries have been found that contain both coordinates and country information, and these have been written in country_and_coordinates_data.json.txt.")

# Bήμα 6: Ενα συνοδευτικό pie chart για τα αποτελέσματα με κλεμμένο κώδικα από το προηγούμενο σκριπτ.

no_data = total_registries - total_geo_registries
sizes = [total_geo_registries, no_data]
labels = ["registries with country and coordinates","no data"]
colors = ["blue", "red"]

plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, autopct= lambda pct: f"{pct:.1f}% ({int(pct / 100. * sum(sizes))})", startangle=90, colors = ["blue","red"])
plt.title("Ποσοστό δειγμάτων με ή χωρίς γεωγραφική πληροφορία πηγής απομονώσεως")
# συμβολοσειρά της μορφής "42.3% (152)"
# lambda pct: f"" καλεί συνάρτηση
# {pct:.1f}%: υπολογίζει ποσοστό με .1 δεκαδικο ψηφιο
# pct / 100. * sum(sizes) μετατρέπει ποσοστό σε απόλυτο αριθμό
# int μετατρέπει απόλυτο αριθμό σε ακέραιο
plt.figtext(0.5, 0.03, f"Σύνολο δειγμάτων: {total_registries}", ha='center', fontsize=10)
plt.tight_layout()
plt.savefig("countries_and_coordinates_pie_chart.png")
plt.show()

