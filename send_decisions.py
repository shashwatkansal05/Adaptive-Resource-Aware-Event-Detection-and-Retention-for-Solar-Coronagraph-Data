import csv
import time
import serial

PORT = "COM3"
BAUD_RATE = 115200
INPUT_FILE = "lasco_decisions.csv"

print("========================================")
print("   SOLAR RETENTION SERIAL SENDER")
print("========================================")
print(f"Port: {PORT}")
print(f"Input: {INPUT_FILE}")
print()

# Open serial connection
ser = serial.Serial(
    PORT,
    BAUD_RATE,
    timeout=1
)

time.sleep(2)

print("Connected to ESP32")
print()

with open(INPUT_FILE, newline="") as f:

    data = list(csv.DictReader(f))

    for row in data:

        frame = int(
            row["frame"]
            .replace("diff_", "")
            .replace(".png", "")
        )

        confidence = float(row["confidence"])
        mode = row["mode"]

        if mode == "FULL":
            cost = 3

        elif mode == "REDUCED":
            cost = 2

        elif mode == "SUMMARY":
            cost = 1

        else:
            cost = 0

        command = (
            f"FRAME,{frame},"
            f"{confidence:.3f},"
            f"{mode},"
            f"{cost}\n"
        )

        print(
            f"Sending: "
            f"FRAME={frame} | "
            f"CONFIDENCE={confidence:.3f} | "
            f"MODE={mode}"
        )

        ser.write(command.encode())

        # Give ESP32 time to process
        time.sleep(0.5)

        # Read ESP32 response
        while ser.in_waiting:

            response = ser.readline().decode(
                errors="ignore"
            ).strip()

            if response:
                print(f"ESP32: {response}")

        print()

ser.close()

print("========================================")
print("Transmission complete.")
print("========================================")
