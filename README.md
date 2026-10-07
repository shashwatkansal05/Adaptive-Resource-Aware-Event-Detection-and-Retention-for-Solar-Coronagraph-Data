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
