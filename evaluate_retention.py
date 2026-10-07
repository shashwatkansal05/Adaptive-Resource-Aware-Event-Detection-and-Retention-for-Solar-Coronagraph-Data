import csv

INPUT_FILE = "lasco_decisions.csv"

data = list(csv.DictReader(open(INPUT_FILE)))

total_frames = len(data)

# Simulated storage costs
FULL_COST = 3
REDUCED_COST = 2
SUMMARY_COST = 1

baseline_cost = total_frames * FULL_COST

adaptive_cost = 0

for row in data:
    mode = row["mode"]

    if mode == "FULL":
        adaptive_cost += FULL_COST
    elif mode == "REDUCED":
        adaptive_cost += REDUCED_COST
    elif mode == "SUMMARY":
        adaptive_cost += SUMMARY_COST

high_confidence = [
    r for r in data
    if float(r["confidence"]) >= 0.70
]

preserved_high_confidence = [
    r for r in high_confidence
    if r["mode"] != "DROP"
]

reduction = (1 - adaptive_cost / baseline_cost) * 100

print("========================================")
print("   ADAPTIVE RETENTION EVALUATION")
print("========================================")

print(f"Total frames              : {total_frames}")
print(f"Baseline storage cost     : {baseline_cost}")
print(f"Adaptive storage cost     : {adaptive_cost}")
print(f"Simulated reduction       : {reduction:.1f}%")

print()
print(f"FULL frames               : {sum(r['mode']=='FULL' for r in data)}")
print(f"REDUCED frames            : {sum(r['mode']=='REDUCED' for r in data)}")
print(f"SUMMARY frames            : {sum(r['mode']=='SUMMARY' for r in data)}")
print(f"DROP frames               : {sum(r['mode']=='DROP' for r in data)}")

print()
print(f"High-confidence events    : {len(high_confidence)}")
print(f"High-confidence preserved : {len(preserved_high_confidence)}")

if high_confidence:
    preservation = (
        len(preserved_high_confidence)
        / len(high_confidence)
        * 100
    )
else:
    preservation = 0

print(f"Event preservation        : {preservation:.1f}%")

print()
print("========================================")
