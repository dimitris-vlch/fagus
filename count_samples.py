import json
import sys

json_to_be_calculated = sys.argv[1]

with open(json_to_be_calculated, "r", encoding="utf-8") as file:
    samples = json.load(file)

samples_count = len(samples)

print(f": {samples_count}")
