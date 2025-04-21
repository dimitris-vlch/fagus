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

# Βήμα 8: Απλοποίηση του πεδίου country_submitted, ώστε να περιέχει μοναχά την χώρα χωρίς την παρουσία επιπλέον πληροφοριών.
# για κάθε πεδίο του country_submitted, εφαρμόζουμε την συνάρτηση: lambda x: x.split(":")[0].split()[0].
# .split(":")[0] κρατάει οτι υπάρχει πριν την άνω-κάτω τελεία.
# .strip() αφαιρεί περιττά κένα πριν και μετά.

for registry in data:
    registry["country_submitted"] = registry["country_submitted"].split(":")[0].strip()

# Bήμα 9: Για κάθε εγγραφή κρατάμε μονάχα τα πεδία lat, lon, country_submited

# Η στρατιγική μας. Δημιουργούμε μια κενή λίστα country_and_coordinates_data στην οποία στο τέλος θα την γεμίσουμε με .append(geo_registry). Δημιουργούμε το geo_registry μεσα σε μια for με την παραπάνω συνθήκη if για να βάλουμε μονάχα τα κατάλληλα δείγματα. Στην συνέχεια φτιάχνουμε geo_registry = {"πεδιο" registry.get("πεδιο")}   

country_and_coordinates_data = []

for idx, registry in enumerate(data,1): 
# τροποποιούμε λιγο το for registry in data: για να χουμε καταμέτρηση δειγμάτων με idx & enumarate
    if registry.get("lat") and registry.get("lon") and registry.get("country_submitted"):
        geo_registry = {
            "Registry number:" : idx,         
            "sample_accession" : registry["sample_accession"],
            "lat" : registry["lat"],
            "lon" : registry["lon"],
            "country_submitted" : registry["country_submitted"]
        }
        country_and_coordinates_data.append(geo_registry)

# Βήμα 10: Παρασκευή json αρχείου που περιέχει μόνο τα δεδομένα που μας ενδιαφέρουν.

with open("country_and_coordinates_minimal_data.json.txt", "w", encoding = "utf-8") as file:
    json.dump(country_and_coordinates_data, file, indent = 2, ensure_ascii= False )

# Βήμα 11: Aνακοίνωση αποτελεσμάτων στον κένσορα:

print (f"\ncountry_and_coordinates_minimal_data.json.txt has been created successfully. This json file contains {len(country_and_coordinates_data)} registries with both country and coordinates and only these fields from the whole registry, as well as the sample_accession field for identification\n")

### Έλεγχος της εγκυρότητας των γεωγραφικών δεδομένων μέσω της βιβλιοθήκης geo_pandas

# Βήμα 12: Ορισμός dataframe. Μετατρέπουμε την λίστα country_and_coordinates_data σε dataframe. Μετατρέπει το json σε πίνακα

dataframe = pd.DataFrame(country_and_coordinates_data)

# Βήμα 13: Στον πίνακα dataframe προσθέτουμε μια νέα στήλη, coordinates_point. Η στήλη περιέχει ένα γεωμετρικό σημείο Point(lon, lat). 
# η .apply() χρησιμοποιείται για να εφαρμόσουμε μια συνάρτηση σε κάθε στοιχείο ενός πίνακα pandas.
# Με axis=1 η συνάρτηση .apply() εφαρμόζεται σε κάθε γραμμή του πίνακα ενώ με axis=0 σε κάθε στήλη.
# Με lambda row: Εφαρμόζουμε την συνάρτηση για κάθε γραμμή του πίνακα.
# Με float() μετατρέπουμε string σε φυσικό αριθμό για να μη βγαλει error η shapely. float("34.74") → 34.74
# Mε row αναφεράμαστε για κάθε στήλη του dataframe
# Με Point ορίζουμε σημείο (x,y)

dataframe["coordinates_point"] = dataframe.apply(lambda row: Point(float(row["lon"]), float(row["lat"])), axis=1)

# Βήμα 14: Κατασκευή ενός GeoDataFrame. Εναν πίνακα pandas, που αναγνωρίζει χωρικά αντικείμενα όπως Point. 
# Ορίζουμε ένα gpd.GeoDataFrame() με όρισμα:
# Το Dataframe που αξιοποιούμε
# geometry = dataframe["coordinates_point"] την στήλη του dataframe που περιέχει την γεωγραφική πληροφορία.
# crs="EPSG:4326" Το σύστημα συντεταγμένων που αξιοποιείται.

geo_dataframe = gpd.GeoDataFrame(dataframe, geometry = dataframe["coordinates_point"], crs = "EPSG:4326")

# Βήμα 15: Καλούμε έτοιμο geodataframe της geopandas, το naturalearth_lowres
# Η geopandas έχει έτοιμο geodataset τον παγκόσμιο χάρτη σε χαμηλή ανάλυση. Ο χάρτης περιέχει πολύγωνα που περιγράφουν το σχήμα, τα σύνορα της κάθε χώρας.
# gpd.read_file(...) διαβάζει την τοποθεσία που παίρνει από το gpd.datasets.get_path και την μετατρέπει σε geodataframe.
# δυστυχώς δεν είναι προεγκατεστημένος ο χάρτης και πρέπει να τον κατεβάσουμε και να ορίσουμε το path.


geopandas_naturalearth_lowres = gpd.read_file("/home/dimitris/Documents/Github my repo/fagus/ne_110m_admin_0_countries")

# Βήμα 16: Επεξεργασία naturalearth_lowres
# φορτώνω τον χάρτη natural_lowres.
# με .explode() καλύτερη απεικονιση νησιωτικών συμπλεγμάτων.
# index_parts=False: και .reset_index(drop=True): είναι τυπικά, για να δουλέψει σωστά ο κώδικας.

geopandas_geo_dataframe = geopandas_naturalearth_lowres.explode(index_parts=False).reset_index(drop=True)

# με τις τυπικές αυτές αλλαγές, ο κώδικας θα δουλέψει καλύτερα.
#print(geopandas_naturalearth_lowres[["name", "geometry"]].head())
#print(geopandas_geo_dataframe[["name", "geometry"]].head())


# Βήμα 11: Ενώση των 2 geodataframes, των geopandas_geo_dataframe και geo_dataframe
# η .sjoin είναι συνάρτηση της geopandas για χωρική ένωση. Για κάθε σημείο point που έχουμε ορίσει στο πρώτο dataset geo_dataframe, το αντιστοιχεί στο πολύγωνο geopandas_geo_dataframe.
# how = "left" ωστε να κρατάμε όλα τα σημεία από το geo_dataframe, ακόμα και αν αυτά δεν αντιστοιχούν σε κάποια χώρα.
# με predicate = "" καθορίζεται ο τύπος της χωρικής ένωσης. Με within, ελέγχεται αν τα σημεία του πρώτου, ανήκουν στο πολύγωνο του δεύτερου.

combined_geo_dataframe = gpd.sjoin(geo_dataframe, geopandas_geo_dataframe, how = "left", predicate = "within")

# το combined_geo_dataframe έχει και μια στήλη ADMIN, που είναι η χώρα από το geopandas_geo_dataframe, καθώς και τη στήλη country από το geo_dataframe.

# Βήμα 17: Προετοιμασία λίστας curated_data που θα χρησιμοποιηθεί για το json αρχείο.
# δημιουργία κενής λίστας curated_data, στην οποία και στην συνέχεια θα γράψουμε τα απαραίτητα πεδία για κάθε λεξικότ της.
# στην for, ορίζουμε και _, το _ παίρνει την τιμή του index που προσφέρει το dataframe, αλλά εμείς αυτό δεν το χρειαζόμαστε εδώ και το αγνοούμε.
# η .iterrows() είναι κλασσική μέθοδος για να πάρουμε τα ενα πίνακα pandas και να τον κάνουμε μεταβλητή.
# με την append.() αντιστοιχούμε κάθε γραμμή (row) σε ένα λεξικό της curated_data.

print("Available columns in geo_joined:\n", combined_geo_dataframe.columns.tolist())


curated_data = []

for _, row in combined_geo_dataframe.iterrows():
    curated_data.append({
        "Registry number:": row["Registry number:"],
        "sample_accession": row["sample_accession"],
        "lat": row["lat"],
        "lon": row["lon"],
        "country_submitted": row["country_submitted"],
        "country_suggested_from_coordinates": row["ADMIN"]
    })

# Βήμα 18: Εγγραφή σε json αρχείο , ανακοίνωση των αποτελεσμάτων στον κένσορα.

with open("countries_and_coordinates_curation.json.txt", "w",encoding="utf-8") as file:
    json.dump(curated_data, file, indent = 2, ensure_ascii= False)

print(f"\ncountries_and_coordinates_curation.json.txt was created successfully!")