#script to merge all the text in one file

import os
import pandas as pd

dataset_path = "dataset"
output_file = os.path.join(dataset_path, "merged_posts.txt")

csv_files = [f for f in os.listdir(dataset_path) if f.endswith(".csv")]

with open(output_file, "w", encoding="utf-8") as out:
    for csv in csv_files:
        full_path = os.path.join(dataset_path, csv)
        try:
            df = pd.read_csv(full_path)

            if 'post' in df.columns:
                texts = df['post'].dropna().astype(str)
                for line in texts:
                    clean_line = line.strip().replace('\n', ' ')
                    out.write(clean_line + "\n")
                print(f" Processed: {csv}")
            else:
                print(f" 'post' column missing in: {csv}")

        except Exception as e:
            print(f" Failed to process {csv}: {e}")

print(f"\n Final merged text saved at: {output_file}")
