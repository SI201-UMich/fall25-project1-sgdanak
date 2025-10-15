import csv

def open_csv(filename): 
    with open(filename, mode='r') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    return data 

filename = "penguins.csv"
penguins = open_csv(filename)

# for row in penguins[:3]:
#     print(row)

def calculate_species_percentage(data):
    island_counts = {}
    total_counts = {}

    for row in data:
        island = row['island']
        species = row['species']
        sex = row['sex']

        if island not in island_counts:
            island_counts[island] = {}
        if species not in island_counts[island]:
            island_counts[island][species] = {}
        if sex not in island_counts[island][species]:
            island_counts[island][species][sex] = 0
        
        island_counts[island][species][sex] += 1

        if island not in total_counts:
            total_counts[island] = {}
        if sex not in total_counts[island]:
            total_counts[island][sex] = 0
        total_counts[island][sex] += 1

#calculating percentages

    percentages = {}
    for island in island_counts:
        percentages[island] = {}
        for species in island_counts[island]:
            percentages[island][species] = {}
            for sex in island_counts[island][species]:
                total = total_counts[island][sex]
                count = island_counts[island][species][sex]
                if total > 0:
                    percentages[island][species][sex] = round((count / total) * 100, 2)
    return percentages

filename = "penguins.csv"
penguins = open_csv(filename)

result = calculate_species_percentage(penguins)

for island, species_data in result.items():
    print(f"\nIsland: {island}")
    for species, sex_data in species_data.items():
        print(f" Species:{species}")
        for sex, pct in sex_data.items():
            print(f"  {sex.capitalize()}: {pct}%")