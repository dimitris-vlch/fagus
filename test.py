import json
import matplotlib.pyplot as plt 
import geopandas as gpd 
import pandas as pd 
from shapely.geometry import Point 
from geopy.geocoders import Nominatim  
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg


with open("country_and_coordinates_minimal_data.json.txt", "r", encoding= "utf-8") as file:
    country_and_coordinates_data = json.load(file)

dataframe = pd.DataFrame(country_and_coordinates_data)

dataframe["coordinates_point"] = dataframe.apply(lambda row: Point(float(row["lon"]), float(row["lat"])), axis=1)

geo_dataframe = gpd.GeoDataFrame(dataframe, geometry = dataframe["coordinates_point"], crs = "EPSG:4326")

geopandas_naturalearth_lowres = gpd.read_file("/home/dimitris/Documents/Github my repo/fagus/ne_110m_admin_0_countries")

geopandas_geo_dataframe = geopandas_naturalearth_lowres.explode(index_parts=False).reset_index(drop=True)

combined_geo_dataframe = gpd.sjoin(geo_dataframe, geopandas_geo_dataframe, how = "left", predicate = "within")


with open("curated_data_json.txt", "r", encoding="utf-8")as file:
    curated_data = json.load(file)

# Οπτικοποίηση των αποτελεσμάτων:

# Γιατί ήταν σημαντικές οι παραπάνω διορθώσεις;

# Διάγραμμα 1: Bar Plot που συγκρίνει τον αριθμό των αποτελεσμάτων mismatch ύστερα από την επεξεργασία των συντεταγμένων με τον geopandas χάρτη πολυγώνων naturalearth_lowres, τον αριθμό των mismatch μετά την διόρθωση για Σερβία, τον αριθμό των mismatch μετά την διόρθωση για ΗΠΑ και τον αριθμό των mismatch μετά την συμπλήρωση χώρας με Nominatim για τις συντεταγμένες που δεν εντοπίζονται στο χάρτη naturalearth_lowres.

# Yπολογίζω mismatches αποκλειστικά με geopandas, δεν έχουμε άκομα ανιχνεύσει καμία ψευδώς θετική αναντιστοιχία χώρας-συντεταγμένων:

calculated_mismatches_1 = 0
false_positive_mismatches = 0 

for _, row in combined_geo_dataframe.iterrows():
    country_match = "yes" if row["country_submitted"] == row["ADMIN"] else "no"
    if country_match == "no":
        calculated_mismatches_1 += 1

false_positive_mismatches = calculated_mismatches_1 - calculated_mismatches_1 # we havent used a method yet to calculate mismatches.

print(f"\nΥπολογίζοντας αποκλειστικά με geopandas, βρίσκω {calculated_mismatches_1} αναντιστοιχίες χώρας-συντεταγμένων και ανιχνεύω {false_positive_mismatches} ψευδώς θετικές αναντιστοιχίες")

calculated_mismatches_2 = 0
false_positive_mismatches = 0 

# Υπολογίζω mismatches με geopandas και πραγματοποιώ την διόρθωση για ΗΠΑ

for _, row in combined_geo_dataframe.iterrows():
    
    suggested = row["ADMIN"]
    
    if suggested == "United States of America":
        suggested = "USA"
    
    country_match = "yes" if row["country_submitted"] == row["ADMIN"] or row["country_submitted"] == suggested else "no"
    
    if country_match == "no":
        calculated_mismatches_2 += 1

false_positive_mismatches = calculated_mismatches_1 - calculated_mismatches_2

print(f"\nΥπολογίζοντας με geopandas και διορθώνοντας για ΗΠΑ, βρίσκω {calculated_mismatches_2} αναντιστοιχίες χώρας-συντεταγμένων και ανιχνεύω {false_positive_mismatches} ψευδώς θετικές αναντιστοιχίες")

# Υπολογίζω mismatches με geopandas και πραγματοποιώ την διόρθωση για ΗΠΑ και Σερβία

calculated_mismatches_3 = 0
false_positive_mismatches = 0 


for _, row in combined_geo_dataframe.iterrows():
    
    suggested = row["ADMIN"]
    
    if suggested == "United States of America":
        suggested = "USA"
    elif suggested == "Republic of Serbia":
        suggested = "Serbia"
        country_match = "yes" if row["country_submitted"] == suggested else "no"

    country_match = "yes" if row["country_submitted"] == row["ADMIN"] or row["country_submitted"] == suggested else "no"
    
    if country_match == "no":
        calculated_mismatches_3 += 1

false_positive_mismatches = calculated_mismatches_1 - calculated_mismatches_3

print(f"\nΥπολογίζοντας με geopandas, και διορθώνοντας για ΗΠΑ και Σερβία, βρίσκω {calculated_mismatches_3} αναντιστοιχίες χώρας-συντεταγμένων και ανιχνεύω {false_positive_mismatches} ψευδώς θετικές αναντιστοιχίες")

false_positive_mismatches = 0 

match = 0
mismatch = 0

for registry in curated_data:
    if registry["country_match"] == "yes":
        match +=1
    else:
        mismatch +=1


false_positive_mismatches = calculated_mismatches_1 - mismatch

print(f"\nΥπολογίζοντας με geopandas και  και διορθώνοντας για ΗΠΑ και Σερβία, βρίσκω {mismatch} αναντιστοιχίες χώρας-συντεταγμένων και ανιχνεύω {false_positive_mismatches} ψευδώς θετικές αναντιστοιχίες")

# Ονόματα για τα 4 ζευγάρια
labels = [
    "Geopandas (αρχικά)",
    "Geopandas + ΗΠΑ",
    "Geopandas + ΗΠΑ + Σερβία",
    "Geopandas + Nominatim + ΗΠΑ + Σερβία"
]

# Υψος κύριων bars (mismatches)
mismatches = [
    calculated_mismatches_1,
    calculated_mismatches_2,
    calculated_mismatches_3,
    mismatch
]

# Υψος συνοδευτικών bars (false positives που διορθώθηκαν σε κάθε βήμα)
false_positives = [
    calculated_mismatches_1 - calculated_mismatches_1,
    calculated_mismatches_1 - calculated_mismatches_2,
    calculated_mismatches_1 - calculated_mismatches_3,
    calculated_mismatches_1 - mismatch,
] 

# Πίνακας τύπου numpy, len(labels) 4 αφού έχουμε 4 ζευγάρια labels.
x = np.arange(len(labels)) 

width = 0.35 # Πάχος της μπάρας
width = 0.35 # Πλάτος της μπάρας

fig, ax = plt.subplots(figsize=(10, 6)) # Πλαίσιο fig και άξονες ax για το γράφημα

# Για κάθε label, αντιστοιχούν 2 μπάρες.
# x - width/2, μετακινεί την μπάρα λίγο αριστερά από το κέντρο της θέσης
# x + width/2, μετακινεί την μπάρα λίγο δεξιά από το κέντρο της θέσης
# Ύψος μπάρας είναι τα mismatches
# Το πλάτος κάθε μπαρας είναι το 35% δια του 2 του διαθέσιμου κενού.
# label το όνομα της κάθε μπάρας και color το χρώμα

bars1 = ax.bar(x - width/2, mismatches, width, label='Αναντιστοιχίες (Mismatch)', color='skyblue') # Μπάρες mismatches

bars2 = ax.bar(x + width/2, false_positives, width, label='Ψευδώς θετικές που διορθώθηκαν', color='orange') # Μπάρες false positives

# Τίτλοι και ετικέτες
# ax.set_ylabel() τίτλος για άξονα y
# ax.set_title () τίτλος γραφήματος
# ax.set_xticks(x) βάζει ετικέτες στις θέσεις 0, 1, 2, 3
# ax.set_xticklabels() βάζει ετικέτες την μεταβλητή που ορίζουμε
# ax.legend() τοποθετεί υπόμνημα με τα ονόματα των μπαρών και το χρώμα τους. διαβάζει τα labels στο ax.bar(...)), και τα αντίστοιχα χρώματά τους.


ax.set_ylabel("Registries", fontsize=12)
ax.set_title("Περιορισμοί geopandas & αναγκαιότητα βελτιστοποίησης \nγια τον εντοπισμό ψευδών θετικών αναντιστοιχιών", fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=20)
ax.legend()

# Εμφάνιση αριθμού δειγμάτων πάνω από κάθε μπάρα:
# Ορίζουμε πρώτα εξωτερικό loop για κάθε μπάρα mismatch & false positive και έπειτα εσωτερικό loop όλες τις μπάρες μαζί.
# Που θα τοποθετηθεί το νούμερο στον άξονα χ; στην θέση bar.get_x() για να δηλώσουμε την θέση να είναι ίδια με την θέση που ξεκινάει η μπάρα στο άξονα χ
# bar.get_width()/2.0  Με αυτή την οδηγία το κείμενο στοιχίζεται γύρω από το μέσο της μπάρας.
# yval = bar.get_height() Εδώ το yval είναι η τίμη του ύψους της μπάρας, δηλαδή οι τιμές mismatches και false_positives.
# int(yval) μετατρέπει την τιμή yval σε ακέραιο αριθμό. 
# yval + 1 στην θέση αυτή βάζουμε που θα εμφανίζεται το κείμενο. Λίγο πάνω (ένα) από το ύψος της μπάρας.
# va='bottom' vertical allignment, στοίχιση κειμένου δηλαδή ακριβώς κάτω από την θέση που δηλώνουμε.
# ha='center' horizontal allignment, στοίχιση κειμένου γύρω από το μέσο της θέσης που δηλώνουμε.
# Συνολικά: Η τιμή θα τοποθετηθεί στό μέσο της μπάρας και λίγο ποιό πάνω από την κορυφή της.

for bars in [bars1, bars2]:
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1, int(yval), ha='center', va='bottom', fontsize=10)


# Βάζουμε logo-python:
# Κατεβάζω logo: https://www.pngegg.com/en/png-cmbei
# Με 3 κλάσεις matplotlib from matplotlib.offsetbox import OffsetImage, AnnotationBbox και import matplotlib.image as mpimg

# Φορτώνω εικόνα 
python_logo = mpimg.imread('png-clipart-python-others-text-logo')  

# Δημιουργία image box
imagebox = OffsetImage(python_logo, zoom=0.2)  # zoom για να μικρύνει
ab = AnnotationBbox(imagebox, (2.5, max(mismatches)+20), frameon=False)  # Τοποθέτηση στο γράφημα

ax.add_artist(ab)


plt.tight_layout()
plt.savefig("mismatch_curation_bar_plot.png")
plt.show()


