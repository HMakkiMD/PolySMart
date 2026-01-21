# 🧪 Polymer Compatibilization – Data and Analysis  
### *Dynamic Linkages Are Not Required for Polymer Compatibilization by Covalent Crosslinkers*

This repository contains the data and analysis scripts supporting the results presented in the manuscript:

> **Dynamic Linkages Are Not Required for Polymer Compatibilization by Covalent Crosslinkers**  
> Amirhossein Gooranorimi, Liliia Pestereva, Chongkai Zhao,  
> Seyyed Mohammad Mousavifard, Ellie Tupper, Hesam Makki,  
> Chaoying Wan, and Jeremy E. Wulff.

---

## 📁 Repository Structure

The repository is organised as follows:

### 1. `Analysis_Scripts/`
This folder contains all scripts used to perform the analyses reported in the manuscript, including data processing and post-simulation analysis.  
A separate `README.md` file within this folder provides detailed instructions on how to run each script and reproduce the results.

---

### 2. Example Systems

All input files and representative output data for two example systems discussed in the paper are provided.

These systems illustrate the full computational workflow and enable reproduction of the key analyses.

---

#### **`PLA–PBAT–XL1_Method1/`**  
Input and output files for the PLA–PBAT system compatibilized with XL1, modelled using *Method 1* as described in the manuscript.

Contents include:
- **`Conversion.xvg`**  
  C–H insertion conversion as a function of reaction loop.
- **Representative structures and force-field files:**  
  `md0.gro`, `md9.gro`, `md18.gro` with corresponding topology files  
  `loop9.itp`, `loop18.itp`, representing reaction loops at 0, 9, and 18  
  (RMD at 0, 9, and 18 ns).
- **`script/`**  
  Python scripts used for setting up and running the simulations.
- **`data/`**  
  MD run files, topologies, and initial configuration (`box.gro`).

---

#### **`PLA–PE–XL3_Method2/`**  
Input and output files for the PLA–PE system compatibilized with XL3, modelled using *Method 2* as described in the manuscript.

Contents include:
- **`Conversion.xvg`**  
  C–H insertion conversion as a function of reaction loop.
- **Representative structures and force-field files:**  
  `md100.gro`, `md500.gro`, `md1000.gro` with corresponding topology files  
  `loop100.itp`, `loop500.itp`, `loop1000.itp`, representing reaction loops at  
  100, 500, and 1000 (RMD at 100, 500, and 1000 ns).
- **`script/`**  
  Python scripts used for setting up and running the simulations.
- **`data/`**  
  MD run files, topologies, and initial configuration (`box.gro`).

---

## 📝 Notes

- All scripts were tested using:
  - Python 3.10  
  - MATLAB 2023  
  - GROMACS  
  - VMD
- Paths in the scripts are relative to the repository root.
- The provided example systems are representative and sufficient to reproduce the key analyses and workflows described in the manuscript.
