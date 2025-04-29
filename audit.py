import os
from collections import Counter

file_path = os.path.join("dataset", "merged_posts.txt")

with open(file_path, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

# Basic stats
total_lines = len(lines)
duplicates = total_lines - len(set(lines))
line_lengths = [len(line) for line in lines]

short_lines = [line for line in lines if len(line) < 20]
long_lines = [line for line in lines if len(line) > 500]

print(f"📊 Total lines: {total_lines}")
print(f"⚠️ Empty or whitespace-only lines removed: {total_lines - len(lines)}")
print(f"🔁 Duplicate lines: {duplicates}")
print(f"🧮 Avg line length: {sum(line_lengths) // len(line_lengths)}")
print(f"📉 Min line length: {min(line_lengths)}")
print(f"📈 Max line length: {max(line_lengths)}")
print(f"🔎 Very short lines (<20 chars): {len(short_lines)}")
print(f"🔍 Very long lines (>500 chars): {len(long_lines)}\n")

# Show some examples
print("🧾 Examples of short lines:")
for line in short_lines[:5]:
    print(f"- {line}")

print("\n📄 Examples of long lines:")
for line in long_lines[:2]:
    print(f"- {line[:100]}... [{len(line)} chars]")
