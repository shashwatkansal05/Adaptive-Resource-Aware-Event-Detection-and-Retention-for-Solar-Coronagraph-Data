import csv

INPUT_FILE = "lasco_confidence_results.csv"
OUTPUT_FILE = "lasco_decisions.csv"

MAX_SLOTS = 10

used_slots = 0

DOWNLINK_EVERY = 8
DOWNLINK_FREE = 4


def choose_mode(confidence, used_slots):

    pressure = used_slots / MAX_SLOTS

    # --------------------------------
    # HIGH-CONFIDENCE EVENT
    # Never completely discard it
    # --------------------------------

    if confidence >= 0.70:

        if pressure < 0.40:
            return "FULL"

        elif pressure < 0.70:
            return "REDUCED"

        else:
            return "SUMMARY"


    # --------------------------------
    # MEDIUM-CONFIDENCE EVENT
    # --------------------------------

    elif confidence >= 0.30:

        if pressure < 0.40:
            return "REDUCED"

        elif pressure < 0.70:
            return "SUMMARY"

        else:
            return "DROP"


    # --------------------------------
    # LOW-CONFIDENCE EVENT
    # --------------------------------

    elif confidence >= 0.05:

        if pressure < 0.70:
            return "SUMMARY"

        else:
            return "DROP"


    # --------------------------------
    # VERY LOW CONFIDENCE
    # --------------------------------

    else:
        return "DROP"


# --------------------------------
# Load confidence results
# --------------------------------

decisions = []

with open(INPUT_FILE) as f:
    data = list(csv.DictReader(f))


# --------------------------------
# Process frames
# --------------------------------

for i, row in enumerate(data, start=1):

    confidence = float(row["confidence"])

    storage_before = used_slots

    pressure = used_slots / MAX_SLOTS

    mode = choose_mode(
        confidence,
        used_slots
    )


    # --------------------------------
    # Storage cost
    # --------------------------------

    if mode == "FULL":
        storage_cost = 3

    elif mode == "REDUCED":
        storage_cost = 2

    elif mode == "SUMMARY":
        storage_cost = 1

    else:
        storage_cost = 0


    # --------------------------------
    # Respect storage limit
    # --------------------------------

    if used_slots + storage_cost > MAX_SLOTS:

        # FULL → REDUCED
        if mode == "FULL":
            mode = "REDUCED"
            storage_cost = 2

        # REDUCED → SUMMARY
        if used_slots + storage_cost > MAX_SLOTS:
            mode = "SUMMARY"
            storage_cost = 1

        # SUMMARY → DROP
        if used_slots + storage_cost > MAX_SLOTS:

            # IMPORTANT:
            # High-confidence events are still
            # represented as SUMMARY when possible.

            mode = "DROP"
            storage_cost = 0


    used_slots += storage_cost


    # --------------------------------
    # Simulated downlink
    # --------------------------------

    if i % DOWNLINK_EVERY == 0:

        used_slots = max(
            0,
            used_slots - DOWNLINK_FREE
        )

        downlink = "DOWNLINK"

    else:
        downlink = ""


    # --------------------------------
    # Print result
    # --------------------------------

    print(
        f"{row['frame']} | "
        f"confidence={confidence:.3f} | "
        f"pressure={pressure:.2f} | "
        f"{mode:8s} | "
        f"storage={used_slots:2d}/{MAX_SLOTS} | "
        f"{downlink}"
    )


    # --------------------------------
    # Save decision
    # --------------------------------

    decisions.append([
        row["frame"],
        f"{confidence:.4f}",
        f"{pressure:.2f}",
        mode,
        storage_before,
        used_slots,
        downlink
    ])


# --------------------------------
# Write decision log
# --------------------------------

with open(OUTPUT_FILE, "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "frame",
        "confidence",
        "pressure_before",
        "mode",
        "storage_before",
        "storage_after",
        "downlink"
    ])

    writer.writerows(decisions)


print()
print(f"Decision log saved to: {OUTPUT_FILE}")
