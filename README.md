# PolySMart
# Introduction
PolySMart is a python package which is designed to perform a reactive MD simulation in GROMACS MD package using MARTINI coarse-grain 
forcefield. It is specially designed to perform polymerization and crosslinking process in order to generate the topology of the 
resulting structure at any stage of the reaction. 
The algorithm utilized in this code package is based on exploring the system for the species that can react (with the conditions which 
had been defined by the user) and taking place the reaction by modifying related topology files followed by energy minimization and a 
short equilibration. These steps are iterated until a specified condition is satisfied.

Publication : [https://doi.org/10.1039/D3MH00088E](https://doi.org/10.1039/D3MH00088E)
## User Guides
[How to Use](https://github.com/HMakkiMD/PolySMart/wiki/How-to-Use)\
[Outputs](https://github.com/HMakkiMD/PolySMart/wiki/Outputs)\
[Prerequisite](https://github.com/HMakkiMD/PolySMart/wiki/Prerequisite)\
[Test Case](https://github.com/HMakkiMD/PolySMart/wiki/Test-Case)
