# Σκριπτάκι για την γραφική αναπαράσταση των αποτελεσμάτων σε Bar και Pie chart

# Βήμα 1: Εισαγωγή βιλβιοθηκών και ανάγνωση του αρχείου json, μετατροπή του σε λεξικό python και υπολογισμός του συνολικού αριθμού των δειγμάτων (total_samples).

# Αξιοποιούμε το υποπακέτο pyplot της βιβλιοθήκης matplotlib. Το plt ειναι alias για matplotlib.pyplot. Το pyplot έχει συναρτήσεις για γραφικά διαγράμματα, bar chart, pie charts, συναρτήσεις για τίτλους και ετικέτες, καθώς και για να εμφανίσεις τα διαγράμματα.
# Εισάγουμε την υποβιβλιοθήκη Counter από την βιβλιοθήκη collections. Το Counter το αξιοποιούμε για να δούμε πόσες φορές εμφανίζεται κάθε τιμή. Μας είναι χρήσιμο επειδή έχουμε πολλά δείγματα και κάθε δείγμα έχει διαφορετικά μεταδεδομένα γεωγραφίας, βλέπουμε απλώς την συχνότητα εμφάνισης της τοποθεσίας, της χώρας κλπ.

import json
import matplotlib.pyplot as plt
from collections import Counter 

with open("results_merged_json.txt", "r", encoding="utf-8") as file:
    data = json.load(file)

total_samples = len(data)

# Βήμα 2: Ορίζουμε ένα λεξικό, geo_fields, οπου κάθε αντικείμενό του (fields) είναι ένα πεδίο των αντικειμένων του λεξικού data, το οποίο και όμως φέρει γεωγραφική πληροφορία. Πεδιά του στύλ χώρα, συντεταγμένες lat, lon, κλπ. Ορίζουμε μια λίστα με χρώματα.

geo_fields = [
    "country", "location", "location_start", "location_end", "isolation_source", "lat", "lon"
]

colors_bar_chart = [
    "#4E79A7",  # Μπλε
    "#F28E2B",  # Πορτοκαλί
    "#E15759",  # Κόκκινο
    "#76B7B2",  # Κυανό-πράσινο
    "#59A14F",  # Πράσινο
    "#EDC948",  # Κίτρινο
    "#B07AA1",  # Μοβ
]

# Βήμα 3: Ορίζουμε τις μεταβλητές που θα χρειαστούμε για την καταμέτρηση. Μεταβλητή with_geo και μεταβλητή without_geo που ορίζονται ως μηδεν, καθώς και μεταβλητή που ορίζεται ως κενή λίστα Counter για να εκτελέσει την καταμέτρηση των αντικειμένων σε λεξικό data.

with_geo = 0
without_geo = 0
frequency = Counter()

# Βήμα 4: Ορίζουμε μεταβλητή registry για κάθε αντικείμενο της λίστας data.
# Για κάθε registry στη λίστα data.
    #  Για κάθε registry στη λίστα data, oρίζουμε μια μεταβλητή hits = False, την οποία και θα κάνουμε σωστή, εαν η εγγραφή περιέχει γεωγραφικό δείγμα
    # Ορίζουμε μεταβλητή geo_field για κάθε πεδίο της λίστας geo_fields που φτιάξαμε.
    # Για κάθε πεδίο (geo_field) της λίστας geo_fields:
    # Ελέγχουμε με .get() σε κάθε registry αν επιστρέφονται τιμή για fields ή εαν επιστρέφεται  "", δηλαδή κενό field.
    #registry.get(geo_field, ""). «Δώσε μου την τιμή για το key field από το λεξικό registry. Αν δεν υπάρχει, δώσε μου κενό string 
    # ("") αντί για σφάλμα.»
    # .strip() αφαιρεί κενά, tabs, newlines από την αρχή και το τέλος της τιμής. Έτσι, δεν θα μετρήσουμε ένα κενό ως έγκυρη τιμή.  
    # Έτσι, η value είναι μια καθαρή γεωγραφική τιμή πχ Greece.
    # Aν η .get() επιστρέφει field, τότε ή hits γίνεται αληθής και ο μετρητής για τα πεδία με την γεωγραφική πληροφορία αυξάνεται κατά ένα.
    # Έτσι, η value είτε παίρνει μια καθαρή γεωγραφική τιμή, είτε ένα κενό string.
    # Εαν η value έχει γεωγραφική τιμή και δεν είναι δηλαδή κενό string,    
    # Εαν η hits είναι αληθής, τότε η with_geo αυξάνεται κατά 1, διαφορετικά η without_geo αυξάνεται κατά μια μονάδα.
    # frequency[geo_field] += 1 Κάθε φορά που εμφανίζεται κάποιο geo_field του geo_fields, αυξάνεται η τιμή του geo_field με το counter κατα μια μονάδα.

for registry in data:
    hits = False
    for geo_field in geo_fields:
        value = registry.get(geo_field, "").strip()
        if value:
            hits = True
            frequency[geo_field] += 1 

    if hits:
        with_geo += 1
    else:
        without_geo += 1

# Βήμα 5: Εκτύπωση ορισμένων βασικών αποτελεσμάτων: Εκτυπώνονται οι τιμές της κάθε μεταβλητής που αντιπροσωπεύει μέγεθος ενδιαφέροντος και στην συνέχεια το ποσοστό αυτού ως προ τοο σύνολο των δειγμάτων με ένα δεκαδικό ψηφίο.
print("\n")
print(f"Total number of samples: {total_samples}, {total_samples / total_samples: .1%}")
print(f"Total number of samples with geological information: {with_geo} {with_geo / total_samples: .1%}")
print(f"Samples without total abscence of geological information: {without_geo} {without_geo / total_samples:.1%}")

# Βήμα 6: Εκτύπωση των αποτελεσμάτων της καταμέτρησης
# for geo_field, count in frequency.items(): Eκτελούμε βρόγχο loop στο αντικείμενο frequency, το οποίο και είναι τύπου Counter.
# .items() Σε λεξικά και σε μεταβλητές τύπου Counter, επιστρέφει σε ζευγάρια (key,value). Έτσι, αφου ολοκληρώθηκε το βήμα 4, θα ισχύει frequency = Counter({ "country": 4435, "lat": 853, "lon": 853, "location": 200 }).
# Δηλαδή θα ισχύει for geo_field, count in frequency.items(): geo_field = "country", count = 4435 geo_field = "lat", count = 853 geo_field = "lon", count = 853 geo_field = "location", count = 200
# geo_field → είναι το όνομα του πεδίου (string)
# count → είναι το πλήθος εμφανίσεων του πεδίου (ακέραιος αριθμός)
# εκτυπώνουμε στην συνέχεια κάθε πεδίο geo_field, συνοδευόμενο από τον ακέραιο αριθμό του count που μετρήσαμε με τη             frequency[geo_field] += 1 

for geo_field, count in frequency.items():
    print(f"Samples with {geo_field}: {count}")

# Βήμα 7: Pie chart
# Καταρχήν ορίζουμε labels, sizes, colors.

labels = ["With Geo Info", "Without Geo Info"]  # Τα ονόματα των δύο κομματιών της πίτας.   
sizes = [with_geo, without_geo] # το μέγεθος του κάθε κομματιού της πίτας
colors = ["blue","red"] # χρώματα των κομματιών της πίτας

# plt.figure(figsize=(6, 6)) Δημιουργεί νέο καμβά (figure) για το γράφημα, και  ορίζει με figsize το μέγεθος του σε ίντσες όπου στην προκειμένη περίπτωση είναι 6*6. Σε pie chart οφείλουμε να είναι τετράγωνες οι διαστάσεις για να μην είναι η πίτα παραμορφωμένη.
# plt.pie(δημιουργεί πίτα με τα μεγέθη της μεταβλητής size, όπως και ορίσαμε παραπάνω.
#   sizes, το κάθε μέγεθος της πίτας είναι ίσο με το αριθμό των δειγμάτων που έχουν και δεν έχουν γεωγραφία αντίστοιχα.
# τα ονόμα των ετικετών (labels) είναι με την ίδια σειρά με τα μεγέθη (sizes)
# autopct="%1.1f%%" για να εμφανιστεί το ποσοστό του κάθε κομματιού πάνω στο διάγραμμα, στη προκειμένη περίπτωση έχουμε έα δεκαδικό ψηφίο καθώς και σύμβολο επί τοις εκατό.
# startangle=90 γωνία εκκίνησης του διαγράμματος της πίτας. 90 μοίρες και είναι όπως ρολοί τις 12:00.
# colors=colors δίνει τα χρώματα όπως και τα ορίσαμε παραπάνω.

plt.figure(figsize=(6, 6))
plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",  
    startangle=90,      
    colors=colors
)

# plt.title ορίζει τίτλο γραφήματος
# plt.tight_layout() ρυθμίζει το layout αυτόματα ώστε να είναι το κάθε στοιχείο του γραφήματος σε σωστή θέση.
# plt.savefig("geo_pie_chart.png") σώζει το γράφημα ως εικόνα .png.
# plt.show() εμφανίζει το γράφημα στην οθόνη.

plt.figtext(0.5, 0.03, f"Σύνολο δειγμάτων: {total_samples}", ha='center', fontsize=10) # σχολιασμός παρακάτω.
plt.title("Ποσοστό δειγμάτων με ή χωρίς γεωγραφική πληροφορία")
plt.tight_layout()
plt.savefig("geo_pie_chart.png")  # αποθήκευση εικόνας
plt.show()

# Bήμα 8: Bar Chart

# Ορίζουμε μεταβλητές για labels, sizes, colours, όπως ακριβώς κάναμε και παραπάνω.

labels = ["With Geo Info", "Without Geo Info"]
sizes = [with_geo, without_geo]
colors = ["blue","red"]

# με .figure ορίζουμε γράφημα, το οποίο και του δίνουμε διαστάσεις figsize 6 επι 4 ίντσες.
# η .bar() δημιουργεί τις μπάρεις του Bar Chart. στο παράδειγμα μας είναι της μορφής .bar(x,y,colors), δηλαδή οι τιμές του  χ άξονα, στη συνέχεια οι τιμές του ψ άξονα και τέλος τα χρώματα των μπαρών.
# με .ylabel() ορίζουμε τον τίτλο του κάθετου άξονα.

plt.figure(figsize=(6,4))
plt.bar(labels, sizes, color=colors)
plt.ylabel("Αριθμός εγγραφών")

# η .figtext() είναι συνάρτηση της matplotlib. Προσθέτει κείμενο στο figure. Οι αριθμοί 0.5 και 0.01 αναφέρονται στην οριζόντια και στην κάθετη θέση του κειμένου και παίρνουν τιμές από 0 μέχρι και 1, από αριστερά προς τα δεξιά και από κάτω προς τα πάνω αντίστοιχα. το ha αναφέρεται στην στοίχιση του κειμένου και πέρνει τιμές center, left, right και fontsize  μέγεθος γραμματοσειράς. 
 
plt.figtext(0.5, 0.03, f"Σύνολο δειγμάτων: {total_samples}", ha='center', fontsize=10)

# Όπως και στο προηγούμενο βήμα, ορίζουμε .title(), .tight_layout(), .savefig(), .show() για τους ίδιους ακριβώς λόγους.

plt.title("Αριθμός δειγμάτων με ή χωρίς γεωγραφική πληροφορία")
plt.tight_layout(rect=[0, 0.05, 1, 1])  # η συγκεκριμένη ρύθμιση για .tight_layout() τραβάει το γράφημα λίγο προς τα πάνω για να κάνει χώρο και για το .figtext() να χωρέσει.
plt.savefig("geo_bar_Chart.png")
plt.show()

# Pie Chart και Bar Chart για την γραφική απεικόνιση των πεδίων του geo_fields. Βλέπουμε ποιά είναι τα πεδία με τα πλουσιότερα γεωγραφικά δεδομένα.

# Βήμα 9: Μετατροπή του αντικειμένου Counter σε λίστες ώστε να μπορούν να αξιοποιηθούν για διαγράμματα. frequency = ["key1":value1, "key2:value2, etc..."]

field_names = list(frequency.keys()) # δημιοργεί λίστα η οποία έχει τα ονόματα των πεδίων του frequency

field_values = list(frequency.values()) # λίστα με τις τιμές των πεδίων του frequency

field_percentages = [ with_geo / total_samples * 100 for field_value in field_values ] # ποσοστά γεωγραφικών δεδομένων ως προς το σύνολο των δειγμάτων με γεωγραφικά δεδομένα. Θέλουμε αριθμητικά ποσοστά τα οποία και θα τα χρησιμοποιήσουμε για την κατασκευή των διαγραμμάτων. Για κάθε τιμή απο την λίστα των τιμών .values(). Συνολικά, φτιάχνουμε μια λίστα με τα αριθμητικά ποσοστά για κάθε πεδίο που επιθυμούμε να αναπαραστίσουμε.
# επειδή είναι έκφραση και όχι λίστα, έχουμε [] αντι για ().

# Βήμα 10: Διάγραμμα Pie Chart για ποσοστιαία αναπαράσταση του τύπου της γεωγραφικής πληοροφορίας που παρουσιάζεται στα δείγματα, ως προς το σύνολο των δειγμάτων.

plt.figure(figsize=(7, 7))
plt.pie(field_percentages, labels=field_names, startangle=90,  # οπου field_precentages οι τιμές για το διάγραμμα Pue και labels τα ονόματα που συνοδεύουν τις τιμές του field_precentages.
autopct= lambda p: f"{p:.1f}%\n({int(p * total_samples / 100)})", colors=colors_bar_chart) # με λάμδα ορίζουμε μια συνάρτηση. Με p: εμφανίζουμε ποσοστό. Στη πρώτη γραμμή \n έχουμε ποσοστό p με ένα δεκαδικο ψηφίο .1f% το f{} μάλλον χρείαζεται για το συντακτικό απλά. Στη δεύτερη γραμμή, από το ποσοστά field_precentages θα υπολογίσουμε ξανά τις τιμές field_values, διότι η lambda συνάρτση δεν έχει πρόσβαση στην λίστα αυτή. Η συνάρτηση int μετατρέπει ένα κλάσμα σε ακέραιο αριθμό.
plt.title("Γραφική, ποσοστιαία αναπαράσταση της συχνότητας εμφάνισης\n(του τύπου της γεωγραφικής πληροφορίας)\n(ως προς το σύνολο των δειγμάτων)")
plt.tight_layout() #ορίζει αυτόματα το layout.
plt.figtext(0.5, 0.02, f"Σύνολο δειγμάτων: {total_samples}", ha="center", fontsize=10) # λεζάντα κάτω από το γράφημα, όπως περιγράφεται παραπάνω. 
plt.savefig("field_precentages_pie_chart.png")
plt.show()

plt.figure(figsize=(9,5))
plt.bar(field_names, field_values, color=colors_bar_chart) #σε .bar() δεν ορίζουμε ως labels=   
plt.ylabel("Συχνότητα εμφάνισης γεωγραφικής πληροφορίας.")
plt.title("Bar Chart για τη συχνότητα των πεδίων με γεωγραφική πληροφορία")
plt.xticks(rotation=30) # περιστρέφει ετικέτες στο χ αξονα κατα 30 μοίρες ώστε να μην επικαλύπτονται όταν αυτές είναι πολύ μεγάλες.
plt.figtext(0.5, 0.01, f"Σύνολο δειγμάτων: {total_samples}", ha="center", fontsize=10) # λεζάντα στο κάτω μέρος του γραφήματος που αναφέρει τον συνολικό αριθμό των δειγμάτων.
plt.savefig("geo_fields_bar_chart.png")
plt.show()



