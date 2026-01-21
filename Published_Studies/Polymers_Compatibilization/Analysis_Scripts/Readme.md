# 🔬 Supporting Codes for Analysis

This folder contains all scripts used for the analyses reported in the manuscript.  
The codes are provided in both **MATLAB** and **Python** implementations.

---

## 📄 File Descriptions

### 1. `itp_excel.py`
Converts a `.itp` file into an Excel spreadsheet.

**Generated sheets:**
- **`atoms`**  
  Contains all data from the `[ atoms ]` section of the `.itp` file.
- **`bonds_constraints`**  
  Contains data from the `[ bonds ]` and `[ constraints ]` sections.  
  *(Only bead connectivity is included; bond constants are omitted.)*

---

### 2. `analasis_all.m`
Main MATLAB script that integrates all other MATLAB and Python-based scripts.

**Workflow:**
1. Converts `.itp` to Excel using `itp_excel.py`.
2. Uses MATLAB graph functions to identify all connected beads based on connectivity.
3. Generates a `network[number].xlsx` file, where each column corresponds to one cluster of connected beads.

---

### 3. `analasis_all_python.py`
Python implementation of the main analysis pipeline.

**Generated files:**
- `analysis.xlsx`
- `analysis_mw.xlsx`

The calculations are based on **bead number patterns** and **resname identifiers**  
(e.g. `PBAT`, `PLA`, `PET`, `XL1/2`, `XL3/4`).  
These should be updated according to the specific polymer system under study.  
Relevant lines in the code are commented for guidance.

#### Sheet descriptions

**`PDI_bead`**
- Columns (left to right):  
  Mw, Mn, dispersity index (DI), calculated from bead numbers.

**`reacted_clusters`**
| Column | Description |
|--------|-------------|
| 1 | Number of clusters |
| 2 | Number of PLA chains |
| 3 | Number of PBAT/PE chains |
| 4 | Number of crosslinkers |

**Example:**
1   6   2   7
38  1   1   1

Interpretation:
- First row: 1 cluster containing 6 PLA, 2 PBAT/PE, and 7 crosslinkers.
- Second row: 38 clusters, each containing 1 PLA, 1 PBAT/PE, and 1 crosslinker.

**`gMBCPs_composition`**
Shows the composition of heteroclusters:  
- First number: PLA count  
- Second number: PBAT or PE count (depending on system)

---

### 4. `mw_mn_pdi.py`
Calculates Mw, Mn, and dispersity index (DI) based on bead masses.

---

### 5. `renumbering_pbat.py` / `renumbering_pe.py`
Analyzes first-order loops and crosslinker connectivity.

**Example output:**
| No. of PBAT-CL-PBAT connections = 199 |
| No. of PLA-CL-PLA connections = 120 |
| No. of PBAT-CL-PLA connections = 81 |
| No. of first order loops = 21 |

**Interpretation:**
- 199 crosslinkers connect PBAT on both sides.
- 120 crosslinkers connect PLA on both sides.
- 81 crosslinkers connect PLA on one side and PBAT on the other.
- 21 crosslinkers form first-order loops.

---

### 6. `size_gmbcp.m`
Generates an Excel file listing bead numbers for all gMBCPs.
- Each column corresponds to one gMBCP.

---

## 📝 Notes

- Most codes were originally written in **MATLAB**.
- Several scripts were converted to **Python** using AI-assisted tools (ChatGPT) and fully verified.
- Some scripts require minor system-specific adjustments (e.g. `resname` values).  
  See comments within each script for guidance.

---

## ▶️ Usage

1. Place the `.itp` file and required input data in the working directory.
2. Modify system-specific parameters following the comments in the scripts.
3. Run:
analasis_all.m
4. Outputs are generated in **Excel** or **TXT** formats.

---

## 📌 Citation

If you use these scripts in your work, please cite the associated manuscript and dataset accordingly.

