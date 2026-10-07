# Adaptive Resource-Aware Event Detection and Retention for Solar Coronagraph Data

A resource-aware data retention system for solar coronagraph imagery that reduces storage requirements while preserving high-value solar observations under constrained storage and downlink conditions.

## Overview

Space-based instruments can continuously generate large volumes of scientific data, while onboard storage and communication resources remain limited. This creates a need for intelligent data-retention strategies that can determine which observations should be preserved at different levels of fidelity.

This project implements a prototype **resource-aware solar data retention system** using real solar coronagraph observations from the **SOHO/LASCO mission**.

The system analyzes consecutive solar images using running-difference analysis, estimates the amount of observed change, and combines this confidence with simulated storage pressure to select one of four retention modes:

- **FULL** – retain the complete observation
- **REDUCED** – retain a reduced representation
- **SUMMARY** – retain a lightweight summary
- **DROP** – discard the observation

The retention controller is integrated with an **ESP32** to provide a hardware-in-the-loop representation of constrained onboard storage and downlink behavior.


---

## Project Objective

To design and evaluate a resource-aware system that can:

1. Process real solar coronagraph imagery.
2. Detect significant changes between consecutive observations.
3. Estimate an observation confidence/change score.
4. Adapt retention decisions according to both observation significance and storage pressure.
5. Reduce simulated storage requirements.
6. Preserve observations classified as high-confidence.
7. Integrate the decision system with an ESP32 hardware-in-the-loop setup.

---

## System Architecture

```text
                 Real SOHO/LASCO Images
                           │
                           ▼
              Running-Difference Analysis
                           │
                           ▼
                 Confidence Estimation
                           │
                           ▼
              Adaptive Retention Controller
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
           Event       Storage        Resource
          Confidence   Pressure        State
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                  Retention Decision
                           │
          ┌────────┬───────┼────────┬────────┐
          ▼        ▼       ▼        ▼
        FULL    REDUCED  SUMMARY   DROP
                           │
                           ▼
                    ESP32 via UART
                           │
                           ▼
              Storage / Downlink Model
```
# Dataset

The project uses real observations from the Large Angle and Spectrometric Coronagraph (LASCO) instrument aboard the SOHO (Solar and Heliospheric Observatory) spacecraft.

LASCO observes the solar corona by blocking the bright solar disk, allowing structures such as coronal mass ejections (CMEs) and other large-scale coronal features to be observed.

The project uses LASCO imagery as the actual input data.

- Dataset: SOHO/LASCO observations

# Processing Pipeline
1. Running-Difference Analysis

Consecutive LASCO images are converted to grayscale and compared pixel-by-pixel.

For consecutive frames:

Difference = |Current Frame - Previous Frame|

This highlights changes occurring between observations.

2. Confidence Estimation

The running-difference image is analyzed to estimate the amount of significant image change.

The resulting score is normalized to a range suitable for the retention controller.

The score represents the amount of detected change and is used as a decision signal.

The confidence value in this project should not be interpreted as a scientifically validated probability of a solar event.

3. Adaptive Retention

The controller considers both:
```text
Observation Confidence
        +
Current Storage Pressure
        ↓
Retention Decision
```
The system can select one of four retention modes:

# Mode	Purpose
FULL-	Preserve the complete observation
REDUCED-	Preserve a reduced representation
SUMMARY-	Preserve lightweight information
DROP-	Discard low-value observation

This allows the system to adapt its data-retention behavior as available storage decreases.

ESP32 Hardware-in-the-Loop

The retention controller communicates with an ESP32 through a serial UART connection.
```text
Linux / Python Controller
          │
          │ UART
          │ 115200 baud
          ▼
        ESP32
          │
          ▼
 Simulated Storage State
```
The ESP32 maintains a simulated storage capacity of:

Maximum storage = 10 slots

Different retention modes consume different amounts of storage.

A simulated downlink event periodically releases storage space, allowing the system to continue accepting new observations.

This provides a hardware-in-the-loop representation of resource constraints without requiring actual spacecraft storage or communication hardware.

# Experimental Results

The final test sequence contained 12 original LASCO images, producing 11 frame-to-frame differences.
```
Retention Decisions
Retention Mode	Number
FULL	           1
REDUCED	         2
SUMMARY          4
DROP	           4
Total	          11

Simulated Storage
Metric	              Result
Baseline storage cost	  33
Adaptive storage cost	  11
Simulated reduction	   66.7%

Physical File Storage
Metric	               Result
Original PNG size	    4.082 MB
Retained data size	  0.518 MB
Physical reduction	   87.3%
Reduction ratio	      7.89×

High-Confidence Preservation

Using the project's confidence threshold:

- High-confidence observations = 4
- Preserved observations       = 4
- Preservation rate            = 100%
- ESP32 Integration
- UART baud rate        : 115200
- Storage capacity      : 10 slots
- Decision records      : 11/11 transferred
- Automatic downlink    : Enabled
- Downlink release      : 4 slots
```
 # Technologies Used
- Python
- NumPy
- PIL / Pillow
- CSV-based data processing
- Linux
- ESP32
- Arduino
- UART / Serial Communication
- Image Processing
- Resource-aware Decision Making
