# In order for the script to work successfully, run the following commands on bash terminal consequetively.

# python3 coordinatinates_country_curation.py
# python3 coordinatinates_country_curation.py
# python3 coordinatinates_country_curation.py

# note coordinatinates_country_curation.py. The script coordinatinates_country_curation.py takes a while to be completed, so it would be wise for it to be separated from the other the other parts of the script.

# Φτιάχνουμε ένα σκριπτάκι που ελέγχει τις γεωγραφικές συντεταγμένες της κάθε καταχώρησης, για το κατα πόσο αντιστοιχούν στην χώρα που έχει δηλωθεί. θεωρείται ότι αρκετές φορές ο ερευνητής κατά την συμπλήρωση των πεδίων των καταχωρήσεων, ενδεχομένως να μπερδέψει το latitude με το lontitude, η να συμπληρώσει την χώρα που εντοπίζεται το ερευνητικό ίδρυμα, αντί της χώρας συλλογής του δείγματος. Αυτοί και άλλοι λόγοι, επισημαίνουν την ανάγκη πραγματοποίησης της διόρθωσης αυτής στα μεταδεδομένα καταχωρήσεων του δείγματος.

# Bήμα 1: Εισαγωγή βιβλιοθηκών. matplotlib για διάγραμμα pie chart.

# Η geopandas μας επιτρέπει να δουλεύουμε με γεωμετρικά αντικείμενα (σημεία, γραμμές, πολύγωνα) μέσα σε dataframe.
# Η βιβλιοθήκη pandas χρησιμοποείται για δεδομένα σε πίνακες και θα φορτώσουμε μέσω αυτής το json αρχείο.
# Η γνωστή pycountry, έχει τα επίσημα ISO codes των χωρών.
# Η βιβλιοθήκη shapely δουλεύει με γεωμετρικά σχήματα. Από αυτή εισάγουμε το αντικείμενο Point. Θα μετατρέψουμε τα lat & lot σε σημεία στο χώρο (γεωμετρικά). Τα οποία θα τα επεξεργαστούμε σε GeoPandas.

import json
import matplotlib.pyplot as plt 
import geopandas as gpd 
import pandas as pd 
from shapely.geometry import Point 
from geopy.geocoders import Nominatim  
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

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

# Βήμα 6: Επεξεργασία του country_and_coordinates_data.json.txt : αλλαγή της ονομασίας του πεδίου country σε country submitted.

for registry in data:
    registry["country_submitted"] = registry.pop("country", "") # το country φεύγει και μπαίνει country_submitted.

# Βήμα 8: Απλοποίηση του πεδίου country_submitted, ώστε να περιέχει μοναχά την χώρα χωρίς την παρουσία επιπλέον πληροφοριών.
# για κάθε πεδίο του country_submitted, εφαρμόζουμε την συνάρτηση: lambda x: x.split(":")[0].split()[0].
# .split(":")[0] κρατάει οτι υπάρχει πριν την άνω-κάτω τελεία.
# .strip() αφαιρεί περιττά κένα πριν και μετά.

for registry in data:
    registry["country_submitted"] = registry["country_submitted"].split(":")[0].strip()

# Bήμα 7: Για κάθε εγγραφή κρατάμε μονάχα τα πεδία lat, lon, country_submited

# Η στρατιγική μας. Δημιουργούμε μια κενή λίστα country_and_coordinates_data στην οποία στο τέλος θα την γεμίσουμε με .append(geo_registry). Δημιουργούμε το geo_registry μεσα σε μια for με την παραπάνω συνθήκη if για να βάλουμε μονάχα τα κατάλληλα δείγματα. Στην συνέχεια φτιάχνουμε geo_registry = {"πεδιο" registry.get("πεδιο")}   

country_and_coordinates_data = []

for idx, registry in enumerate(data,1): 
# τροποποιούμε λιγο το for registry in data: για να χουμε καταμέτρηση εγγραφών με idx & enumarate
    if registry.get("lat") and registry.get("lon") and registry.get("country_submitted"):
        geo_registry = {
            "Registry number:" : idx,         
            "sample_accession" : registry["sample_accession"],
            "lat" : registry["lat"],
            "lon" : registry["lon"],
            "country_submitted" : registry["country_submitted"]
        }
        country_and_coordinates_data.append(geo_registry)

# Βήμα 8: Παρασκευή json αρχείου που περιέχει μόνο τα δεδομένα που μας ενδιαφέρουν.

with open("country_and_coordinates_minimal_data.json.txt", "w", encoding = "utf-8") as file:
    json.dump(country_and_coordinates_data, file, indent = 2, ensure_ascii= False)

# Βήμα 9: Aνακοίνωση αποτελεσμάτων στον κένσορα:

print (f"\ncountry_and_coordinates_minimal_data.json.txt has been created successfully. This json file contains {len(country_and_coordinates_data)} registries with both country and coordinates and only these fields from the whole registry, as well as the sample_accession field for identification.\n")

### Έλεγχος της εγκυρότητας των γεωγραφικών δεδομένων μέσω της βιβλιοθήκης geo_pandas

# Βήμα 10: Ορισμός dataframe. Μετατρέπουμε την λίστα country_and_coordinates_data σε dataframe. Μετατρέπει το json σε πίνακα

dataframe = pd.DataFrame(country_and_coordinates_data)

# Βήμα 11: Στον πίνακα dataframe προσθέτουμε μια νέα στήλη, coordinates_point. Η στήλη περιέχει ένα γεωμετρικό σημείο Point(lon, lat). 
# η .apply() χρησιμοποιείται για να εφαρμόσουμε μια συνάρτηση σε κάθε στοιχείο ενός πίνακα pandas.
# Με axis=1 η συνάρτηση .apply() εφαρμόζεται σε κάθε γραμμή του πίνακα ενώ με axis=0 σε κάθε στήλη.
# Με lambda row: Εφαρμόζουμε την συνάρτηση για κάθε γραμμή του πίνακα.
# Με float() μετατρέπουμε string σε φυσικό αριθμό για να μη βγαλει error η shapely. float("34.74") → 34.74
# Mε row αναφεράμαστε για κάθε στήλη του dataframe
# Με Point ορίζουμε σημείο (x,y)

dataframe["coordinates_point"] = dataframe.apply(lambda row: Point(float(row["lon"]), float(row["lat"])), axis=1)

# Βήμα 12: Κατασκευή ενός GeoDataFrame. Εναν πίνακα pandas, που αναγνωρίζει χωρικά αντικείμενα όπως Point. 
# Ορίζουμε ένα gpd.GeoDataFrame() με όρισμα:
# Το Dataframe που αξιοποιούμε
# geometry = dataframe["coordinates_point"] την στήλη του dataframe που περιέχει την γεωγραφική πληροφορία.
# crs="EPSG:4326" Το σύστημα συντεταγμένων που αξιοποιείται.

geo_dataframe = gpd.GeoDataFrame(dataframe, geometry = dataframe["coordinates_point"], crs = "EPSG:4326")

# Βήμα 13: Καλούμε έτοιμο geodataframe της geopandas, το naturalearth_lowres
# Η geopandas έχει έτοιμο geodataset τον παγκόσμιο χάρτη σε χαμηλή ανάλυση. Ο χάρτης περιέχει πολύγωνα που περιγράφουν το σχήμα, τα σύνορα της κάθε χώρας.
# gpd.read_file(...) διαβάζει την τοποθεσία που παίρνει από το gpd.datasets.get_path και την μετατρέπει σε geodataframe.
# δυστυχώς δεν είναι προεγκατεστημένος ο χάρτης και πρέπει να τον κατεβάσουμε και να ορίσουμε το path.


geopandas_naturalearth_lowres = gpd.read_file("/home/dimitris/Documents/Github my repo/fagus/ne_110m_admin_0_countries")

# Βήμα 14: Επεξεργασία naturalearth_lowres
# φορτώνω τον χάρτη natural_lowres.
# με .explode() καλύτερη απεικονιση νησιωτικών συμπλεγμάτων.
# index_parts=False: και .reset_index(drop=True): είναι τυπικά, για να δουλέψει σωστά ο κώδικας.

geopandas_geo_dataframe = geopandas_naturalearth_lowres.explode(index_parts=False).reset_index(drop=True)

# με τις τυπικές αυτές αλλαγές, ο κώδικας θα δουλέψει καλύτερα.
#print(geopandas_naturalearth_lowres[["name", "geometry"]].head())
#print(geopandas_geo_dataframe[["name", "geometry"]].head())


# Βήμα 15: Ενώση των 2 geodataframes, των geopandas_geo_dataframe και geo_dataframe
# η .sjoin είναι συνάρτηση της geopandas για χωρική ένωση. Για κάθε σημείο point που έχουμε ορίσει στο πρώτο dataset geo_dataframe, το αντιστοιχεί στο πολύγωνο geopandas_geo_dataframe.
# how = "left" ωστε να κρατάμε όλα τα σημεία από το geo_dataframe, ακόμα και αν αυτά δεν αντιστοιχούν σε κάποια χώρα.
# με predicate = "" καθορίζεται ο τύπος της χωρικής ένωσης. Με within, ελέγχεται αν τα σημεία του πρώτου, ανήκουν στο πολύγωνο του δεύτερου.

combined_geo_dataframe = gpd.sjoin(geo_dataframe, geopandas_geo_dataframe, how = "left", predicate = "within")

# το combined_geo_dataframe έχει και μια στήλη ADMIN, που είναι η χώρα από το geopandas_geo_dataframe, καθώς και τη στήλη country από το geo_dataframe.

# Βήμα 16: Προετοιμασία λίστας curated_data που θα χρησιμοποιηθεί για το json αρχείο.
# δημιουργία κενής λίστας curated_data, στην οποία και στην συνέχεια θα γράψουμε τα απαραίτητα πεδία για κάθε λεξικότ της.
# στην for, ορίζουμε και _, το _ παίρνει την τιμή του index που προσφέρει το dataframe, αλλά εμείς αυτό δεν το χρειαζόμαστε εδώ και το αγνοούμε.
# η .iterrows() είναι κλασσική μέθοδος για να πάρουμε τα ενα πίνακα pandas και να τον κάνουμε μεταβλητή.
# με την append.() αντιστοιχούμε κάθε γραμμή (row) σε ένα λεξικό της curated_data.
# πεδίο country_match, ελέγχει αν τα δύο πεδία των χωρών είναι ίδια.
# print("Available columns in geo_joined:\n", combined_geo_dataframe.columns.tolist())
# Το βημα 16 βρίσκεται στο mismatches_and_reverse_geocoding.py


# Επιδιόρθωση σφάλματος 1: Η Σερβία γράφεται από τον geopandas_naturalearth_lowres ως Republic of Serbia, ενώ η ΗΠΑ γράφεται United States of America. Επομένως, μέσα στην for, αν η row["ADMIN"] δίνει τις τιμές United States of America και Republic of Serbia, μετανομάνται σε USA και Serbia. Στην συνέχεια ακολουθεί εκ νέου έλεγχος αντιστοίχησης, αυτή τη φορά όμως δίκαιος, τα αποτελέσματα έχουν τωρα την ευκαιρία να γίνουν δεκτά.

# Επιδιόρθωση σφάλματος 2: Ο χάρτης που αξιοποιήσαμε δεν παρέχει γεωγραφικές συντεταγμένες για Νορβηγία.
# Χρήση LLM για την εξαγωγή λίστας συντεταγμένων που δεν έχουν αντιστοιχίσει σε χώρες.
# Αρχικά, απομόνωση των συντεταγμένων οι οποίες και δεν αντιστοιχούν σε χώρα:

# Οι επιδιορθώσεις επειδή είναι αρκετές γραμμές κώδικα, γίνονται στο αρχείο mismatches_and_reverse_geocoding.py.

# Βήμα 17: Φόρτωση αρχείου curated_data_json.txt, το οποίο παράγεται από των κώδικα του coordinatinates_country_curation.py.

with open("curated_data_json.txt", "r", encoding="utf-8")as file:
    curated_data = json.load(file)

# Bήμα 18: Γραφική απεικόνιση των αποτελεσμάτων: Pie chart.

colors_bar_chart = [
    "#4E79A7",  # Μπλε
    "#F28E2B",  # Πορτοκαλί
    "#E15759",  # Κόκκινο
    "#76B7B2",  # Κυανό-πράσινο
    "#59A14F",  # Πράσινο
    "#EDC948",  # Κίτρινο
    "#B07AA1",  # Μοβ
]

# Οπτικοποίηση των αποτελεσμάτων:

# Διάγραμμα 1: Pie Chart Εγγραφές που διαθέτουν πληροφορία χώρας και συντεταγμένων συγκριτικά με τις εγγραφές που δεν διαθέτουν ταυτόχρονα και τις 2 πληροφορίες συντεταγμένων ή χώρας, ή καμία από τις 2 πληροφορίες.

no_data = total_registries - total_geo_registries
sizes = [total_geo_registries, no_data]
labels = ["registries with country and coordinates","no data"]
colors = ["blue", "red"]

fig = plt.figure(figsize=(6, 6)) # ορίζω fig = ώστε μετά να έχω προσβασε σε fig.add_axes() για την τροποποίηση της θέσης του λόγκο.
plt.pie(sizes, labels=labels, autopct= lambda pct: f"{pct:.1f}% ({int(pct / 100. * sum(sizes))})", startangle=90, colors = ["blue","red"])
plt.title("Ποσοστό εγγραφών με ή χωρίς γεωγραφική πληροφορία χώρας και συντεταγμένων.")
# συμβολοσειρά της μορφής "42.3% (152)"
# lambda pct: f"" καλεί συνάρτηση
# {pct:.1f}%: υπολογίζει ποσοστό με .1 δεκαδικο ψηφιο
# pct / 100. * sum(sizes) μετατρέπει ποσοστό σε απόλυτο αριθμό
# int μετατρέπει απόλυτο αριθμό σε ακέραιο
plt.figtext(0.5, 0.03, f"Σύνολο εγγραφών: {total_registries}", ha='center', fontsize=12)

# Python-logo
python_logo = mpimg.imread('png-clipart-python-others-text-logo.png')  
imagebox = OffsetImage(python_logo, zoom=0.1)  # zoom για να μικρύνει
logo_ax = fig.add_axes([0.89, -0.02, 0.1, 0.1], anchor='NE', zorder=1, facecolor = 'white')
logo_ax.imshow(python_logo)
logo_ax.axis('off')

plt.tight_layout()
plt.savefig("countries_and_coordinates_pie_chart.png")
plt.show()

#Το Διάγραμμα 2 (Pie Chart) παρουσιάζει τα αποτελέσματα της σύγκρισης ανάμεσα στη χώρα που έχει δηλωθεί ως τόπος προέλευσης ενός δείγματος και στη χώρα που προκύπτει από τις δηλωμένες γεωγραφικές συντεταγμένες. Η επεξεργασία των συντεταγμένων γίνεται με χρήση των βιβλιοθηκών Geopandas και Nominatim, μέσω της διαδικασίας του reverse geocoding. Στο γράφημα περιλαμβάνονται μόνο οι εγγραφές που φέρουν ταυτόχρονα και δηλωμένη χώρα και γεωγραφικές συντεταγμένες. 

match = 0
mismatch = 0

for registry in curated_data:
    if registry["country_match"] == "yes":
        match +=1
    else:
        mismatch +=1

print(f"\n {match} matches and {mismatch} mismatches")

sizes = [match, mismatch]
labels = ["coordinates alligning with country","faulty coordinates or country"]
colors = ["blue", "red"]

fig = plt.figure(figsize=(6, 6)) # ορίζω fig = ώστε μετά να έχω προσβασε σε fig.add_axes() για την τροποποίηση της θέσης του λόγκο.
plt.pie(sizes, labels=labels, autopct= lambda pct: f"{pct:.1f}% ({int(pct / 100. * sum(sizes))})", startangle=00, colors = ["blue","red"])
plt.title("Εγγραφές με συντεταγμένες που συμφωνούν με την δηλωμένη χώρα συγκριτικα με εγγραφές που διαφωνούν")
plt.figtext(0.5, 0.02, f"Σύνολο εγγραφών: {total_registries}", ha='center', fontsize=12)
plt.figtext(0.5, 0.07, f"Σύνολο εγγραφών με συντεγμένες και χώρα: {len(curated_data)}", ha='center', fontsize=12)

# Python-logo
python_logo = mpimg.imread('png-clipart-python-others-text-logo.png')  
imagebox = OffsetImage(python_logo, zoom=0.1)  # zoom για να μικρύνει
logo_ax = fig.add_axes([0.89, -0.02, 0.1, 0.1], anchor='NE', zorder=1, facecolor = 'white')
logo_ax.imshow(python_logo)
logo_ax.axis('off')

plt.tight_layout()
plt.savefig("countries_and_coordinates_pie_chart.png")
plt.show()
