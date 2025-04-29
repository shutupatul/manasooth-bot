import os

file_path = os.path.join("dataset", "merged_posts.txt")
cleaned_path = os.path.join("dataset", "cleaned_posts.txt")

with open(file_path, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

unique_lines = list(set(lines))
filtered = [
    line for line in unique_lines
    if 20 <= len(line) <= 2000  # you can adjust max length if needed
]

print(f"Original lines: {len(lines)}")
print(f"Unique lines: {len(unique_lines)}")
print(f"Filtered lines (20–2000 chars): {len(filtered)}")

with open(cleaned_path, "w", encoding="utf-8") as f:
    for line in filtered:
        f.write(line + "\n")

print(f"\n✅ Cleaned dataset written to: {cleaned_path}")
