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



calculated_mismatches_1 = 0
false_positive_mismatches = 0 

for _, row in combined_geo_dataframe.iterrows():
    country_match = "yes" if row["country_submitted"] == row["ADMIN"] else "no"
    if country_match == "no":
        calculated_mismatches_1 += 1

print(f"\nΥπολογίζοντας αποκλειστικά με geopandas, βρίσκω {calculated_mismatches_1} αναντιστοιχίες χώρας-συντεταγμένων και ανιχνεύω {false_positive_mismatches} ψευδώς θετικές αναντιστοιχίες")

calculated_mismatches_2 = 0

# Υπολογίζω mismatches με geopandas και πραγματοποιώ την διόρθωση για ΗΠΑ

for _, row in combined_geo_dataframe.iterrows():
    
    suggested = row["ADMIN"]
    
    if suggested == "United States of America":
        suggested = "USA"
    
    country_match = "yes" if row["country_submitted"] == row["ADMIN"] or row["country_submitted"] == suggested else "no"
    
    if country_match == "no":
        calculated_mismatches_2 += 1

false_positive_mismatches = calculated_mismatches_1 - calculated_mismatches_2

print(f"\nΥπολογίζοντας αποκλειστικά με geopandas, βρίσκω {calculated_mismatches_2} αναντιστοιχίες χώρας-συντεταγμένων και ανιχνεύω {false_positive_mismatches} ψευδώς θετικές αναντιστοιχίες")

    
