from pathlib import Path
from PIL import Image
import csv


# -----------------------------------------
# Input / output paths
# -----------------------------------------

INPUT_DIR = Path("data/lasco_sequence/png")

DECISION_FILE = "lasco_decisions.csv"

OUTPUT_DIR = Path("data/lasco_retained")

FULL_DIR = OUTPUT_DIR / "full"
REDUCED_DIR = OUTPUT_DIR / "reduced"
SUMMARY_DIR = OUTPUT_DIR / "summary"


# -----------------------------------------
# Create directories
# -----------------------------------------

FULL_DIR.mkdir(parents=True, exist_ok=True)
REDUCED_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------
# Read controller decisions
# -----------------------------------------

with open(DECISION_FILE) as f:

    decisions = list(csv.DictReader(f))


# -----------------------------------------
# Summary CSV
# -----------------------------------------

summary_file = SUMMARY_DIR / "events.csv"

with open(summary_file, "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "frame",
        "confidence",
        "pressure_before",
        "mode",
        "storage_before",
        "storage_after"
    ])


    # -------------------------------------
    # Process each controller decision
    # -------------------------------------

    for row in decisions:

        frame = row["frame"]

        confidence = float(row["confidence"])

        pressure_before = float(
            row["pressure_before"]
        )

        mode = row["mode"]

        storage_before = int(
            row["storage_before"]
        )

        storage_after = int(
            row["storage_after"]
        )


        # ---------------------------------
        # Convert diff number → LASCO image
        # ---------------------------------

        index = int(
            frame.replace("diff_", "")
                 .replace(".png", "")
        )

        source_file = (
            INPUT_DIR /
            f"lasco_{index:03d}.png"
        )


        # ---------------------------------
        # Check source image
        # ---------------------------------

        if not source_file.exists():

            print(
                f"{frame} | "
                f"mode={mode:8s} | "
                f"ERROR: source image missing"
            )

            continue


        # ---------------------------------
        # FULL
        # ---------------------------------

        if mode == "FULL":

            output_file = (
                FULL_DIR /
                source_file.name
            )

            img = Image.open(source_file)

            img.save(output_file)

            print(
                f"{frame} | "
                f"confidence={confidence:.3f} | "
                f"mode=FULL     | "
                f"saved={output_file.name}"
            )


        # ---------------------------------
        # REDUCED
        # ---------------------------------

        elif mode == "REDUCED":

            output_file = (
                REDUCED_DIR /
                source_file.name
            )

            img = Image.open(source_file)

            reduced = img.resize(
                (512, 512)
            )

            reduced.save(output_file)

            print(
                f"{frame} | "
                f"confidence={confidence:.3f} | "
                f"mode=REDUCED  | "
                f"saved={output_file.name}"
            )


        # ---------------------------------
        # SUMMARY
        # ---------------------------------

        elif mode == "SUMMARY":

            writer.writerow([
                frame,
                f"{confidence:.4f}",
                f"{pressure_before:.2f}",
                mode,
                storage_before,
                storage_after
            ])

            print(
                f"{frame} | "
                f"confidence={confidence:.3f} | "
                f"mode=SUMMARY  | "
                f"metadata saved"
            )


        # ---------------------------------
        # DROP
        # ---------------------------------

        elif mode == "DROP":

            print(
                f"{frame} | "
                f"confidence={confidence:.3f} | "
                f"mode=DROP     | "
                f"not retained"
            )


print()
print("Retention processing complete.")
print(f"Decision rows processed: {len(decisions)}")
