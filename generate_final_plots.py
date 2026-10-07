import csv
from pathlib import Path
import matplotlib.pyplot as plt


DECISIONS = "lasco_decisions.csv"
ORIGINAL_DIR = Path("data/lasco_sequence/png")
RETAINED_DIR = Path("data/lasco_retained")


# ============================================================
# LOAD DATA
# ============================================================

with open(DECISIONS, newline="") as f:
    data = list(csv.DictReader(f))


frames = [
    int(r["frame"].replace("diff_", "").replace(".png", ""))
    for r in data
]

confidence = [
    float(r["confidence"])
    for r in data
]

pressure = [
    float(r["pressure_before"])
    for r in data
]

modes = [
    r["mode"]
    for r in data
]


# ============================================================
# PLOT 1 — CONFIDENCE
# ============================================================

plt.figure(figsize=(9, 5))

plt.plot(
    frames,
    confidence,
    marker="o"
)

plt.axhline(
    0.70,
    linestyle="--",
    label="High-confidence threshold"
)

plt.xlabel("Frame")
plt.ylabel("Confidence")
plt.title("Solar Event Confidence vs Frame")
plt.ylim(0, 1.05)
plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    "confidence_vs_frame.png",
    dpi=300
)

plt.close()


# ============================================================
# PLOT 2 — RETENTION MODE
# ============================================================

mode_values = {
    "DROP": 0,
    "SUMMARY": 1,
    "REDUCED": 2,
    "FULL": 3
}

mode_numeric = [
    mode_values[m]
    for m in modes
]

plt.figure(figsize=(9, 5))

plt.step(
    frames,
    mode_numeric,
    where="mid",
    marker="o"
)

plt.yticks(
    [0, 1, 2, 3],
    ["DROP", "SUMMARY", "REDUCED", "FULL"]
)

plt.xlabel("Frame")
plt.ylabel("Retention Mode")
plt.title("Adaptive Retention Decision")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "retention_mode_vs_frame.png",
    dpi=300
)

plt.close()


# ============================================================
# PLOT 3 — STORAGE PRESSURE
# ============================================================

plt.figure(figsize=(9, 5))

plt.plot(
    frames,
    pressure,
    marker="o"
)

plt.axhline(
    1.0,
    linestyle="--",
    label="Storage limit"
)

plt.xlabel("Frame")
plt.ylabel("Storage Pressure")
plt.title("Storage Pressure Before Each Retention Decision")
plt.ylim(0, 1.05)
plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    "storage_pressure_vs_frame.png",
    dpi=300
)

plt.close()


# ============================================================
# PLOT 4 — PHYSICAL STORAGE
# ============================================================

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

original_mb = original_bytes / 1024 / 1024
retained_mb = retained_bytes / 1024 / 1024

plt.figure(figsize=(7, 5))

plt.bar(
    ["Original", "Retained"],
    [original_mb, retained_mb]
)

plt.ylabel("Storage (MB)")
plt.title("Physical Storage Reduction")

plt.tight_layout()

plt.savefig(
    "physical_storage_comparison.png",
    dpi=300
)

plt.close()


print()
print("================================")
print(" FINAL PLOTS GENERATED")
print("================================")
print()
print("confidence_vs_frame.png")
print("retention_mode_vs_frame.png")
print("storage_pressure_vs_frame.png")
print("physical_storage_comparison.png")
print()
