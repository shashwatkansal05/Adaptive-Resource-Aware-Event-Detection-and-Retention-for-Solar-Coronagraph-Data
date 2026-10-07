from pathlib import Path
from PIL import Image
import numpy as np

INPUT_DIR = Path("data/lasco_sequence/png")
OUTPUT_DIR = Path("data/lasco_sequence/running_diff")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

files = sorted(INPUT_DIR.glob("*.png"))

print(f"Input frames: {len(files)}")

previous = None

for i, file in enumerate(files):

    current = np.array(
        Image.open(file).convert("L"),
        dtype=np.int16
    )

    if previous is None:
        previous = current
        continue

    # Absolute running difference
    diff = np.abs(current - previous)

    # Convert back to 8-bit image
    diff = np.clip(diff, 0, 255).astype(np.uint8)

    output = OUTPUT_DIR / f"diff_{i:03d}.png"

    Image.fromarray(diff).save(output)

    print(
        f"{output.name} | "
        f"mean={diff.mean():.3f} | "
        f"max={diff.max()} | "
        f"changed>10={(diff > 10).sum()}"
    )

    previous = current

print()
print("Running-difference generation complete.")
