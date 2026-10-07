from pathlib import Path
from PIL import Image
import numpy as np
import csv

INPUT_DIR = Path("data/lasco_sequence/running_diff")
OUTPUT_FILE = "lasco_confidence_results.csv"

THRESHOLD = 10

files = sorted(INPUT_DIR.glob("*.png"))

raw_scores = []

# -----------------------------------------
# First pass: calculate raw change scores
# -----------------------------------------

for file in files:

    img = np.array(
        Image.open(file).convert("L")
    )

    changed_pixels = int(
        np.sum(img > THRESHOLD)
    )

    change_ratio = changed_pixels / img.size

    raw_scores.append(
        (file.name, changed_pixels, change_ratio)
    )


# -----------------------------------------
# Normalize score across this sequence
# -----------------------------------------

scores = [
    x[2]
    for x in raw_scores
]

score_min = min(scores)
score_max = max(scores)

print(f"Raw score min = {score_min:.6f}")
print(f"Raw score max = {score_max:.6f}")
print()


results = []

for frame, changed_pixels, raw_score in raw_scores:

    if score_max == score_min:

        confidence = 0.0

    else:

        confidence = (
            (raw_score - score_min)
            / (score_max - score_min)
        )

    confidence = max(
        0.0,
        min(1.0, confidence)
    )

    print(
        f"{frame} | "
        f"changed_pixels={changed_pixels:6d} | "
        f"raw={raw_score:.4f} | "
        f"confidence={confidence:.3f}"
    )

    results.append([
        frame,
        changed_pixels,
        round(raw_score, 6),
        round(confidence, 4)
    ])


# -----------------------------------------
# Save results
# -----------------------------------------

with open(OUTPUT_FILE, "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "frame",
        "changed_pixels",
        "raw_score",
        "confidence"
    ])

    writer.writerows(results)


print()
print(f"Saved results to: {OUTPUT_FILE}")
