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