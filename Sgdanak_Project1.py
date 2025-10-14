import csv

def open_csv(filename): 
    with open(filename, mode='r') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    return data 

filename = "penguins.csv"
penguins = open_csv(filename)

for row in penguins[:3]:
    print(row)

