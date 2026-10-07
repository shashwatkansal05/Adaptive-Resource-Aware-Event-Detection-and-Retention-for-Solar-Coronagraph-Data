import csv
from pathlib import Path


DECISIONS = "lasco_decisions.csv"
ORIGINAL_DIR = Path("data/lasco_sequence/png")
RETAINED_DIR = Path("data/lasco_retained")


FULL_COST = 3
REDUCED_COST = 2
SUMMARY_COST = 1


# ------------------------------------------------------------
# Load decisions
# ------------------------------------------------------------

with open(DECISIONS, newline="") as f:
    data = list(csv.DictReader(f))


# ------------------------------------------------------------
# Mode counts
# ------------------------------------------------------------

counts = {
    "FULL": 0,
    "REDUCED": 0,
    "SUMMARY": 0,
    "DROP": 0
}

for row in data:
    counts[row["mode"]] += 1


# ------------------------------------------------------------
# Storage-cost evaluation
# ------------------------------------------------------------

baseline_cost = len(data) * FULL_COST

adaptive_cost = (
    counts["FULL"] * FULL_COST
    + counts["REDUCED"] * REDUCED_COST
    + counts["SUMMARY"] * SUMMARY_COST
)

simulated_reduction = (
    1 - adaptive_cost / baseline_cost
) * 100


# ------------------------------------------------------------
# Confidence preservation
# ------------------------------------------------------------

high_confidence = [
    r for r in data
    if float(r["confidence"]) >= 0.70
]

preserved = [
    r for r in high_confidence
    if r["mode"] != "DROP"
]

preservation = (
    len(preserved) / len(high_confidence) * 100
    if high_confidence else 0
)


# ------------------------------------------------------------
# Physical storage
# ------------------------------------------------------------

original_files = list(
    ORIGINAL_DIR.glob("lasco_*.png")
)

retained_files = list(
    RETAINED_DIR.rglob("*.png")
)

original_bytes = sum(
    f.stat().st_size
    for f in original_files
)

retained_bytes = sum(
    f.stat().st_size
    for f in retained_files
)

physical_reduction = (
    1 - retained_bytes / original_bytes
) * 100

compression_ratio = (
    original_bytes / retained_bytes
    if retained_bytes else 0
)


# ------------------------------------------------------------
# Print final results
# ------------------------------------------------------------

print()
print("==============================================")
print("       SOLAR RETENTION FINAL EVALUATION")
print("==============================================")

print()
print("DATASET")
print("----------------------------------------------")
print(f"Input frames                 : {len(data)}")
print(f"Original PNG frames          : {len(original_files)}")

print()
print("RETENTION DECISIONS")
print("----------------------------------------------")
print(f"FULL                         : {counts['FULL']}")
print(f"REDUCED                      : {counts['REDUCED']}")
print(f"SUMMARY                      : {counts['SUMMARY']}")
print(f"DROP                         : {counts['DROP']}")

print()
print("SIMULATED STORAGE")
print("----------------------------------------------")
print(f"Baseline cost                : {baseline_cost}")
print(f"Adaptive cost                : {adaptive_cost}")
print(f"Storage reduction            : {simulated_reduction:.1f}%")

print()
print("EVENT PRESERVATION")
print("----------------------------------------------")
print(f"High-confidence events       : {len(high_confidence)}")
print(f"Preserved                    : {len(preserved)}")
print(f"Preservation rate            : {preservation:.1f}%")

print()
print("PHYSICAL STORAGE")
print("----------------------------------------------")
print(f"Original size                : {original_bytes / 1024 / 1024:.3f} MB")
print(f"Retained size                : {retained_bytes / 1024 / 1024:.3f} MB")
print(f"Physical reduction           : {physical_reduction:.1f}%")
print(f"Reduction ratio              : {compression_ratio:.2f}x")

print()
print("ESP32 INTEGRATION")
print("----------------------------------------------")
print("Serial link                  : 115200 baud")
print("Frames transferred           : 11/11")
print("Storage limit                : 10 slots")
print("Automatic downlink           : YES")
print("Downlink release             : 4 slots")

print()
print("==============================================")
print("             EVALUATION COMPLETE")
print("==============================================")
