import json
import matplotlib.pyplot as plt 
from geopy.geocoders import Nominatim 
import geopandas as gpd 
import pandas as pd 
from shapely.geometry import Point
import time

# Κώδικας και βιβλιοθήκες που λειτουργούν ως υπόβαθρο για να τρέξει το σκριπτ.

with open("country_and_coordinates_minimal_data.json.txt", "r", encoding= "utf-8") as file:
    country_and_coordinates_data = json.load(file)

dataframe = pd.DataFrame(country_and_coordinates_data)

dataframe["coordinates_point"] = dataframe.apply(lambda row: Point(float(row["lon"]), float(row["lat"])), axis=1)

geo_dataframe = gpd.GeoDataFrame(dataframe, geometry = dataframe["coordinates_point"], crs = "EPSG:4326")

geopandas_naturalearth_lowres = gpd.read_file("/home/dimitris/Documents/Github my repo/fagus/ne_110m_admin_0_countries")

geopandas_geo_dataframe = geopandas_naturalearth_lowres.explode(index_parts=False).reset_index(drop=True)

combined_geo_dataframe = gpd.sjoin(geo_dataframe, geopandas_geo_dataframe, how = "left", predicate = "within")

# Επιδιόρθωση σφάλματος 1: Η Σερβία γράφεται από τον geopandas_naturalearth_lowres ως Republic of Serbia, ενώ η ΗΠΑ γράφεται United States of America. Επομένως, μέσα στην for, αν η row["ADMIN"] δίνει τις τιμές United States of America και Republic of Serbia, μετανομάνται σε USA και Serbia. Στην συνέχεια ακολουθεί εκ νέου έλεγχος αντιστοίχησης, αυτή τη φορά όμως δίκαιος, τα αποτελέσματα έχουν τωρα την ευκαιρία να γίνουν δεκτά.

curated_data = []

for _, row in combined_geo_dataframe.iterrows():

    suggested = row["ADMIN"]
    country_match = "yes" if row["country_submitted"] == row["ADMIN"] else "no"
    
    if suggested == "United States of America":
        suggested = "USA"
        country_match = "yes" if row["country_submitted"] == suggested else "no"
    elif suggested == "Republic of Serbia":
        suggested = "Serbia"
        country_match = "yes" if row["country_submitted"] == suggested else "no"

    
    curated_data.append({
        "Registry number:": row["Registry number:"],
        "sample_accession": row["sample_accession"],
        "lat": row["lat"],
        "lon": row["lon"],
        "country_submitted": row["country_submitted"],
        "country_suggested_from_coordinates": suggested,
    #   "country_match": "yes" if row["country_submitted"] == row["ADMIN"] else "no"
        "country_match": country_match
    })

# Επιδιόρθωση σφάλματος 2: Ο χάρτης που αξιοποιήσαμε δεν παρέχει γεωγραφικές συντεταγμένες για Νορβηγία.
# Χρήση LLM για την εξαγωγή λίστας συντεταγμένων που δεν έχουν αντιστοιχίσει σε χώρες.
# Αρχικά, απομόνωση των συντεταγμένων οι οποίες και δεν αντιστοιχούν σε χώρα:

coordinates_without_country = []

for registry in curated_data:
    if pd.isna(registry.get("country_suggested_from_coordinates")): # Ελέγχει αν η χώρα είναι NaN με pd.isna() για pandas-style NaN)
        coordinates_without_country.append({
        "lat": registry["lat"],
        "lon": registry["lon"],
        })
    
    #Το if coordinates_without_country: ελέγχει αν η λίστα δεν είναι κενή

if coordinates_without_country:
    
    print(f"\nA total of {len(coordinates_without_country)} registries have been found with coordinates that do not match to any countries. Proceeding to save these coordinates to coordinates_without_country.json.txt")

    with open("coordinates_without_country.json.txt", "w", encoding= "utf-8") as file:
        json.dump(coordinates_without_country, file, indent= 2, ensure_ascii= False)

# reverse geocoding για coordinates_without_country.json.txt: 
# Nominatim μέσω της Python βιβλιοθήκης geopy (openstreetmap)
# η except χρειάζεται διότι ενδεχομένως η διαδικασία να μην λειτουργήσει.
# geolocator.reverse() παίρνει συντεταγμένες lat, lon και επιστρέφει πληροφορίες.
# language="en" διοτι τα ονόματα των χωρών είναι στα αγγλικά.
# μέγιστος χρόνος αναμονής 10 δευτερόλεπτα ώσπου να απαντήσει ο σερβερ.
# το location.raw εμπεριέχει διάφορες πληροφορίες, συμπεριλαμβανομένου του adress. Το adress περιέχει διάφορα πεδία.
# η γραμμή print(f"{i+1}/{len(coords)} | ({lat}, {lon}) → {country}") προσφέρει live μετάδοση στον κένσορα της διαδικασίας για να μη βαριομαστε.
# ο nomatism έχει όριο ένα request το δευτερόλεπτο. εξού και το  time.sleep(1).

if coordinates_without_country:
    print(f"\nReverse geocoding with nominatim initiated. This may take a minute or two.")


    geolocator = Nominatim(user_agent="fagus_country_checker")
    coordinates_with_country_from_nominatim = []

    for i, registry in enumerate(coordinates_without_country):
        lat = float(registry["lat"])
        lon = float(registry["lon"])

        try:
            location = geolocator.reverse((lat, lon), language="en", timeout=10)
            country = location.raw.get("address", {}).get("country", "UNKNOWN")
        except Exception as e:
            country = f"ERROR: {e}"

        print(f"{i+1}/{len(coordinates_without_country)} | ({lat}, {lon}) → {country}")
        time.sleep(1)  # για να μην μας μπλοκάρει το OSM

        coordinates_with_country_from_nominatim.append({
            "lat": lat,
            "lon": lon,
            "country_suggested_by_nominatim": country
        })

    with open("coordinates_with_country_from_nominatim.json.txt", "w", encoding="utf-8") as file:
        json.dump(coordinates_with_country_from_nominatim, file, indent=2, ensure_ascii=False)

    print("\nReverse geocoding has been completed. File 'coordinates_with_country_from_nominatim.json.txt' has been created.")

    # Ένωση των χωρών που βρέθηκαν με το nomatism με το τελικό json αρχείο που περιέχει και τα υπόλοιπα δεδομένα, το curated_data.json.txt

for registry in curated_data:
    for entry in coordinates_with_country_from_nominatim:
        lat_match = float(registry.get("lat")) == float(entry.get("lat"))
        lon_match = float(registry.get("lon")) == float(entry.get("lon"))
        
        if lat_match and lon_match:
            registry["country_match_nominatim"] = entry.get("country_suggested_by_nominatim")
# για κάθε λίστα του curated data, εαν η pandas για country_suggested_from_coordinates επιστρέφει NaN, τότε έαν registry.get("country_match_nominatim") == registry.get("country_submitted"), θα ισχύει registry["country_match"] = "yes"
for registry in curated_data:
    if pd.isna(registry.get("country_suggested_from_coordinates")):
        if registry.get("country_match_nominatim") == registry.get("country_submitted"):
            registry["country_match"] = "yes"

with open("curated_data_json.txt", "w", encoding= "utf-8") as file:
    json.dump(curated_data, file, indent= 2, ensure_ascii= False)

print(f"\ncurated_data_json.txt has been created successfully! This json file is an enhanced version of countries_and_coordinates_curation.json.txt and does not include false positive mismatches")


# Οπτικοποίηση των αποτελεσμάτων:

# Γιατί ήταν σημαντικές οι παραπάνω διορθώσεις;

# Διάγραμμα 1: Bar Plot που συγκρίνει τον αριθμό των αποτελεσμάτων mismatch ύστερα από την επεξεργασία των συντεταγμένων με τον geopandas χάρτη πολυγώνων naturalearth_lowres, τον αριθμό των mismatch μετά την διόρθωση για Σερβία, τον αριθμό των mismatch μετά την διόρθωση για ΗΠΑ και τον αριθμό των mismatch μετά την συμπλήρωση χώρας με Nominatim για τις συντεταγμένες που δεν εντοπίζονται στο χάρτη naturalearth_lowres.

# Yπολογίζω mismatches αποκλειστικά με geopandas, δεν έχουμε άκομα ανιχνεύσει καμία ψευδώς θετική αναντιστοιχία χώρας-συντεταγμένων:

calculated_mismatches = 0
false_positive_mismatches = 0 

for _, row in combined_geo_dataframe.iterrows():
    country_match = "yes" if row["country_submitted"] == row["ADMIN"] else "no"
    if country_match == "no":
        calculated_mismatches += 1

print(f"\nΥπολογίζοντας αποκλειστικά με geopandas, βρίσκω {calculated_mismatches} αναντιστοιχίες χώρας-συντεταγμένων και ανιχνεύω {false_positive_mismatches} ψευδώς θετικές αναντιστοιχίες")

calculated_mismatches = 0
false_positive_mismatches = 0 

# Υπολογίζω mismatches με geopandas και πραγματοποιώ την διόρθωση για ΗΠΑ

for _, row in combined_geo_dataframe.iterrows():
    
    suggested = row["ADMIN"]
    
    if suggested == "United States of America":
        suggested = "USA"
    
    country_match = "yes" if row["country_submitted"] == row["ADMIN"] or row["country_submitted"] == suggested else "no"
    
    if country_match == "no":
        calculated_mismatches += 1

print(f"\nΥπολογίζοντας αποκλειστικά με geopandas, βρίσκω {calculated_mismatches} αναντιστοιχίες χώρας-συντεταγμένων και ανιχνεύω {false_positive_mismatches} ψευδώς θετικές αναντιστοιχίες")

    
