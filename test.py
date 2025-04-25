import json
import matplotlib.pyplot as plt 
import geopandas as gpd 
import pandas as pd 
from shapely.geometry import Point 
from geopy.geocoders import Nominatim  



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

# Εισαγωγή απαραίτητων βιβλιοθηκών
import matplotlib.pyplot as plt
import numpy as np

# Ονόματα για τα 4 ζευγάρια
labels = [
    "Geopandas (αρχικά)",
    "Geopandas + ΗΠΑ",
    "Geopandas + ΗΠΑ+Σερβία",
    "Geopandas + Nominatim"
]

# Υψος κύριων bars (mismatches)
mismatches = [128, 110, 93, 83]

# Υψος συνοδευτικών bars (false positives που διορθώθηκαν σε κάθε βήμα)
false_positives = [0, 18, 17, 10]  # Υπολογισμένα ως διαφορά με προηγούμενο

x = np.arange(len(labels))  # θέσεις για τις μπάρες
width = 0.35  # πλάτος μπάρας

fig, ax = plt.subplots(figsize=(10, 6))

# Μπάρες mismatches
bars1 = ax.bar(x - width/2, mismatches, width, label='Αναντιστοιχίες (Mismatch)', color='skyblue')

# Μπάρες false positives
bars2 = ax.bar(x + width/2, false_positives, width, label='Ψευδώς θετικές που διορθώθηκαν', color='orange')

# Τίτλοι και ετικέτες
ax.set_ylabel("Αριθμός περιπτώσεων", fontsize=12)
ax.set_title("Αναγωγή αναντιστοιχιών και εντοπισμός ψευδώς θετικών κατά τις διορθώσεις", fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=20)
ax.legend()

# Τιμές πάνω από κάθε μπάρα
for bars in [bars1, bars2]:
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1, int(yval), ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()
