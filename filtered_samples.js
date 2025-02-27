const fs = require('fs');

// Βήμα 1: Ανάγνωση του αρχείου JSON με τα δείγματα
const rawData = fs.readFileSync('results_sample_json.txt', 'utf8');
const samples = JSON.parse(rawData);

// Βήμα 2: Μέτρηση του συνολικού αριθμού δειγμάτων (με βάση το πεδίο "sample_accession")
const totalSamples = samples.length;

// Βήμα 3: Φιλτράρισμα των δειγμάτων που δεν περιέχουν γεωγραφικές πληροφορίες
// Δηλαδή, αφαιρούμε τα δείγματα όπου τα πεδία "country", "location_end", "location",
// "location_start" και "isolation_source" είναι όλα κενά (δηλαδή "").
const filteredSamples = samples.filter(sample => {
  return !(
    sample.country === "" &&
    sample.location_end === "" &&
    sample.location === "" &&
    sample.location_start === "" &&
    sample.isolation_source === ""
  );
});

const remainingSamples = filteredSamples.length;
const removedSamples = totalSamples - remainingSamples;

// Βήμα 4: Εμφάνιση των αποτελεσμάτων στον κονσόλα
console.log(`Συνολικός αριθμός δειγμάτων (με βάση το sample_accession): ${totalSamples}`);
console.log(`Αφαιρέθηκαν ${removedSamples} δείγματα (χωρίς γεωγραφικές πληροφορίες).`);
console.log(`Παραμένουν ${remainingSamples} δείγματα.`);

// Βήμα 5: Εγγραφή των παραμεινόμενων δειγμάτων σε νέο αρχείο JSON
fs.writeFileSync('results_sample_json_filtered.json', JSON.stringify(filteredSamples, null, 2)); 