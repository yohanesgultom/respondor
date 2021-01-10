import sys
import csv

_, shelter_input_path, demand_input_path = sys.argv

demands = []
with open(demand_input_path) as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        item, per_person, per_shelter, unit, _, _ = row
        demands.append((item, per_person, per_shelter, unit))

with open(shelter_input_path) as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        shelter, capacity = row
        for d in demands:
            item, per_person, per_shelter, unit = d
            amount = int(float(per_person) * float(capacity)) if per_person else int(per_shelter)
            print('\t'.join([item, str(amount), unit, shelter]))
