# SI 201 Project 1
# Your name: Sophia Danak
# Your student id: 15382496
# Your email: sgdanak@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): Yes
# If you worked with generative AI also add a statement for how you used it.  
#I asked Chatgpt to debug my issues and help me get started writing my functions, particularly my nested dictionaries. As I worked, I had ChatGPT verify and correct my progress. I also used it to assist me in writing my write_results_as_csv and it generated the example data and explained how to write my testcases. 


import csv 
import os
import unittest
import tempfile


def open_csv(filename): 
    with open(filename, mode='r') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    return data 

filename = "penguins.csv"
penguins = open_csv(filename)


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
            percentages[island][species] = {}$
            for sex in island_counts[island][species]:
                total = total_counts[island][sex]
                count = island_counts[island][species][sex]
                if total > 0:
                    percentages[island][species][sex] = round((count / total) * 100, 2)
    return percentages

result = calculate_species_percentage(penguins)

for island, species_data in result.items():
    print(f"\nIsland: {island}")
    for species, sex_data in species_data.items():
        print(f" Species:{species}")
        for sex, pct in sex_data.items():
            print(f"  {sex.capitalize()}: {pct}%")


def calculate_avg_flipper_length(data):
    flipper_sums = {}
    flipper_counts = {}

    for row in data:
        island = row['island']
        species = row['species']
        sex = row['sex']
        flipper = row['flipper_length_mm']

        if not flipper or flipper == "NA":
            continue
        flipper = float(flipper)

        if island not in flipper_sums:
            flipper_sums[island] = {}
            flipper_counts[island] = {}
        if species not in flipper_sums[island]:
            flipper_sums[island][species] = {}
            flipper_counts[island][species] = {}
        if sex not in flipper_sums[island][species]:
            flipper_sums[island][species][sex] = 0
            flipper_counts[island][species][sex] = 0

        flipper_sums[island][species][sex] += flipper
        flipper_counts[island][species][sex] += 1
    
    averages = {}
    for island in flipper_sums:
        averages[island] = {}
        for species in flipper_sums[island]:
            averages[island][species] = {}
            for sex in flipper_sums[island][species]:
                total_length = flipper_sums[island][species][sex]
                count = flipper_counts[island][species][sex]
                if count >0:
                    averages[island][species][sex] = round(total_length /count, 2)
    return averages

filename = "penguins.csv"
penguins = open_csv(filename)
result = calculate_avg_flipper_length(penguins)

for island, species_data in result.items():
    print (f"\nIsland: {island}")
    for species, sex_data in species_data.items():
        print(f" Species: {species}")
        for sex, avg in sex_data.items():
            print(f"  {sex.capitalize()}: {avg} mm")


def write_results_as_csv(file_name, results_dict, value_label):
    with open(file_name, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Island","Species", "Sex", value_label])

        for island, species_data in results_dict.items():
            for species, sex_data in species_data.items():
                for sex, value in sex_data.items():
                    writer.writerow([island, species, sex, value])
    print(f"Results written as CVS to {file_name}")


species_percentages = calculate_species_percentage(penguins)
write_results_as_csv("species_percentages.csv", species_percentages, "Percentage (%)")

flipper_averages = calculate_avg_flipper_length(penguins)
write_results_as_csv("avg_flipper_length.csv", flipper_averages, "Average Flipper Length (mm)")


class TestCalculateSpeciesPercentage(unittest.TestCase):
    # --- General/usual cases ---
    def test_percentages_basic_two_islands(self):
        """General: computes % per (island, sex) bucket correctly."""
        data = [
            {"island": "Dream", "species": "Chinstrap", "sex": "female"},
            {"island": "Dream", "species": "Adelie", "sex": "male"},
            {"island": "Biscoe", "species": "Gentoo", "sex": "female"},
            {"island": "Biscoe", "species": "Gentoo", "sex": "female"},
            {"island": "Biscoe", "species": "Adelie", "sex": "female"},
        ]
        out = calculate_species_percentage(data)
        # Dream: females=1 Chinstrap=100; males=1 Adelie=100
        self.assertEqual(out["Dream"]["Chinstrap"]["female"], 100.00)
        self.assertEqual(out["Dream"]["Adelie"]["male"], 100.00)
        # Biscoe females: total=3 -> Gentoo 2/3=66.67, Adelie 1/3=33.33
        self.assertEqual(out["Biscoe"]["Gentoo"]["female"], 66.67)
        self.assertEqual(out["Biscoe"]["Adelie"]["female"], 33.33)

    def test_percentages_multiple_species_same_bucket(self):
        """General: splits percentages within same (island, sex)."""
        data = [
            {"island": "Torgersen", "species": "Adelie", "sex": "male"},
            {"island": "Torgersen", "species": "Adelie", "sex": "male"},
            {"island": "Torgersen", "species": "Gentoo", "sex": "male"},
        ]
        out = calculate_species_percentage(data)
        # male total=3: Adelie 2/3=66.67, Gentoo 1/3=33.33
        self.assertEqual(out["Torgersen"]["Adelie"]["male"], 66.67)
        self.assertEqual(out["Torgersen"]["Gentoo"]["male"], 33.33)

    # --- Edge cases ---
    def test_percentages_empty_input(self):
        """Edge: empty input returns empty dict."""
        self.assertEqual(calculate_species_percentage([]), {})

    def test_percentages_missing_or_blank_sex_bucket(self):
        """Edge: blank sex forms its own bucket and computes 100%."""
        data = [
            {"island": "Dream", "species": "Adelie", "sex": ""},
            {"island": "Dream", "species": "Adelie", "sex": ""},  # two blanks
            {"island": "Dream", "species": "Gentoo", "sex": ""},
        ]
        out = calculate_species_percentage(data)
        # blank-sex total=3: Adelie 2/3=66.67, Gentoo 1/3=33.33
        self.assertEqual(out["Dream"]["Adelie"][""], 66.67)
        self.assertEqual(out["Dream"]["Gentoo"][""], 33.33)


class TestCalculateAvgFlipperLength(unittest.TestCase):
    # --- General/usual cases ---
    def test_avg_flipper_basic(self):
        """General: computes mean per (island, species, sex)."""
        data = [
            {"island": "Dream", "species": "Adelie", "sex": "male", "flipper_length_mm": "180"},
            {"island": "Dream", "species": "Adelie", "sex": "male", "flipper_length_mm": "190"},
            {"island": "Dream", "species": "Adelie", "sex": "female", "flipper_length_mm": "170"},
        ]
        out = calculate_avg_flipper_length(data)
        self.assertEqual(out["Dream"]["Adelie"]["male"], 185.00)
        self.assertEqual(out["Dream"]["Adelie"]["female"], 170.00)

    def test_avg_flipper_multiple_islands_species(self):
        """General: handles multiple islands/species groups."""
        data = [
            {"island": "Biscoe", "species": "Gentoo", "sex": "female", "flipper_length_mm": "210"},
            {"island": "Biscoe", "species": "Gentoo", "sex": "female", "flipper_length_mm": "200"},
            {"island": "Torgersen", "species": "Adelie", "sex": "male", "flipper_length_mm": "185"},
        ]
        out = calculate_avg_flipper_length(data)
        self.assertEqual(out["Biscoe"]["Gentoo"]["female"], 205.00)
        self.assertEqual(out["Torgersen"]["Adelie"]["male"], 185.00)

    # --- Edge cases ---
    def test_avg_flipper_skips_NA(self):
        """Edge: 'NA' or empty values are skipped; group with only NA disappears."""
        data = [
            {"island": "Biscoe", "species": "Gentoo", "sex": "male", "flipper_length_mm": "NA"},
            {"island": "Biscoe", "species": "Gentoo", "sex": "male", "flipper_length_mm": ""},
            {"island": "Biscoe", "species": "Gentoo", "sex": "female", "flipper_length_mm": "200"},
        ]
        out = calculate_avg_flipper_length(data)
        # male group had only invalids -> no key
        self.assertNotIn("male", out["Biscoe"]["Gentoo"])
        # female group averaged correctly
        self.assertEqual(out["Biscoe"]["Gentoo"]["female"], 200.00)

    def test_avg_flipper_empty_input(self):
        """Edge: empty input returns empty dict."""
        self.assertEqual(calculate_avg_flipper_length([]), {})


class TestWriteResultsAsCSV(unittest.TestCase):
    # --- General/usual cases ---
    def test_write_results_typical(self):
        """General: writes header and all rows from nested dict."""
        results = {
            "Dream": {"Adelie": {"male": 50.0, "female": 50.0}},
            "Biscoe": {"Gentoo": {"female": 66.67}},
        }
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "out.csv")
            write_results_as_csv(path, results, "Percentage (%)")
            # Read back and validate
            with open(path, newline="") as f:
                r = list(csv.reader(f))
            self.assertEqual(r[0], ["Island", "Species", "Sex", "Percentage (%)"])
            rows = {tuple(x) for x in r[1:]}
            self.assertIn(("Dream", "Adelie", "male", "50.0"), rows)
            self.assertIn(("Dream", "Adelie", "female", "50.0"), rows)
            self.assertIn(("Biscoe", "Gentoo", "female", "66.67"), rows)

    def test_write_results_with_different_metric_label(self):
        """General: respects provided value_label."""
        results = {"Torgersen": {"Adelie": {"male": 185.0}}}
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "avg.csv")
            write_results_as_csv(path, results, "Average Flipper Length (mm)")
            with open(path, newline="") as f:
                r = list(csv.reader(f))
            self.assertEqual(r[0], ["Island", "Species", "Sex", "Average Flipper Length (mm)"])
            self.assertEqual(r[1], ["Torgersen", "Adelie", "male", "185.0"])

    # --- Edge cases ---
    def test_write_results_empty_dict_writes_only_header(self):
        """Edge: empty results -> file has only header."""
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "empty.csv")
            write_results_as_csv(path, {}, "Value")
            with open(path, newline="") as f:
                r = list(csv.reader(f))
            self.assertEqual(len(r), 1)
            self.assertEqual(r[0], ["Island", "Species", "Sex", "Value"])

def test_write_results_nonexistent_directory_raises(self):
        """Edge: writing to a missing directory raises FileNotFoundError."""
        missing_dir = os.path.join(tempfile.gettempdir(), "this_dir_should_not_exist_12345")
        path = os.path.join(missing_dir, "out.csv")
        with self.assertRaises(FileNotFoundError):
            write_results_as_csv(path, {"X": {"Y": {"Z": 1}}}, "Value")


if __name__ == "__main__":
    unittest.main()