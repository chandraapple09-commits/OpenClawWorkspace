# Extruder Data Analysis Report

**Source file:** `/Users/chandraprakash/Desktop/apollo extruder project/extruder_data 1.csv`  
**Analyzed on:** 2026-02-08

## 1) Dataset Overview

- Rows: **14,378**
- Columns: **91**
- Time coverage (localized): **2025-12-14 07:01:10** to **2025-12-25 06:58:37**
- Duration: **~11.0 days**
- Machine: **P1011_WTTE0100** (single value in dataset)
- Distinct recipes: **29**

## 2) Sampling / Time Behavior

- Median sample interval: **~3.01 sec**
- 95th percentile interval: **~210.64 sec**

Interpretation: data is mostly high-frequency (~3 sec) with occasional larger gaps.

## 3) Active vs Idle (using screw speed > 1 rpm)

- Extruder 1 active ratio: **60.13%**
- Extruder 2 active ratio: **60.03%**
- Extruder 3 active ratio: **61.50%**

Interpretation: line is active roughly ~60% of recorded time, with significant idle periods.

## 4) Top Recipes by Volume

1. **TR5348_1** – 4,115 rows  
2. **TR5687_1** – 2,020 rows  
3. **TR5811_1** – 1,735 rows  
4. **TR5548_1** – 1,580 rows  
5. **TR5812_1** – 1,526 rows

## 5) Process Relationships (All rows)

Correlation summary:

- Extruder 1: corr(rpm, torque) = **0.971**, corr(rpm, stack pressure) = **0.984**
- Extruder 2: corr(rpm, torque) = **0.965**, corr(rpm, stack pressure) = **0.940**
- Extruder 3: corr(rpm, torque) = **0.939**, corr(rpm, stack pressure) = **0.969**

Interpretation: very strong positive coupling between screw speed and both torque/stack pressure, as expected in stable extrusion behavior.

## 6) Data Quality Findings

### 6.1 Columns mostly/fully empty
A large number of columns are entirely empty in this file (e.g., many Extruder 4/5 fields, head pressures for some extruders, setpoints, preformer/extrudate temperature, etc.).

### 6.2 Negative values detected
Some channels include negative readings (likely sensor noise, reverse movement, or bad samples):

- extruder_2_screw_speed_rpm: **717** negative values (min -1.991)
- extruder_3_screw_speed_rpm: **792** negative values (min -2.385)
- extruder_2_feeder_conv_speed: **49** negative values (min -10.070)
- extruder_3_feeder_conv_speed: **12** negative values (min -10.070)
- extruder_1_torque_current: **2** negative values (min -0.427)

Recommendation: clip tiny negatives near 0 where physically impossible, and flag larger negatives for instrumentation review.

## 7) Typical Operating Ranges (selected, overall)

- extruder_1_screw_speed_rpm: median **14.996**, IQR **0.000 to 16.785**
- extruder_1_torque_current: median **73.358**, IQR **0.000 to 76.849**
- extruder_1_stack_pressure: median **65.195**, IQR **0.519 to 68.980**
- cassette_1_temp: median **89.4°C**
- cassette_2_temp: median **89.0°C**

Interpretation: bimodal-ish behavior from active/idle phases (lower quartile often at/near 0 for speed-linked variables).

## 8) Suggested Next Steps

1. Build a **cleaned analysis table**:
   - Remove empty columns
   - Parse timestamps
   - Clip physically impossible negatives to 0 (or isolate as faults)
2. Create **recipe-wise SPC limits** (rpm, torque, stack pressure, tip temps).
3. Detect **anomalous windows** using rolling z-score / EWMA.
4. Generate dashboards:
   - uptime/idle timeline
   - recipe change timeline
   - correlation drift over time

---

If needed, I can also produce:
- an anomaly list with exact timestamps,
- recipe-wise control limits,
- and a ready-to-run Python script version for repeat daily analysis.
