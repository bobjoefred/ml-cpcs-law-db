from csv_pipeline import generator as gen

from os import walk
import pandas as pd

# Get directory source and all folders within
dir_source, dir_names, _ = next(walk("../input"), (None, None, []))

# Generate csv entries for each folder
all_fields = []
for dir_name in dir_names:
    input_dir = (dir_source + '/' + dir_name)
    print(input_dir)
    all_fields.append(gen.generate_fields(
        input_directory = input_dir,
        officer_roster_csv_path = 'data/officer_roster.csv',
        debug = True))

df = pd.DataFrame(all_fields)
df.to_csv('output.csv', index=False)
