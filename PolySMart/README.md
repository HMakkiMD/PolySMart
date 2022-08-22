# PolySMart
PolySMart is a python package which is designed to perform a reactive MD simulation in GROMACS MD package using MARTINI coarse-grain 
forcefield. It is specially designed to perform polymerization and crosslinking process in order to generate the topology of the 
resulting structure at any stage of the reaction. 
The algorithm utilized in this code package is based on exploring the system for the species that can react (with the conditions which 
had been defined by the user) and taking place the reaction by modifying related topology files followed by energy minimization and a 
short equilibration. These steps are iterated until a specified condition is satisfied.

# Prerequisite
PolySMart requires python version 3.6 or greater and does not use any additional libraries.

# How to Use
In order to perform a reaction you should follow these steps:
## 1. Generate Inputs
All input-related files are placed in "data" folder.
* You need to create an initial configuration file (.gro) of your mixture system, name it "box.gro" and place it in "data" folder.
* Edit file "inputs.txt" according to its help file (these are input information for the process). 
* Edit file "new_angles_parameters.txt" according to its help file (information of new angles which are formed during the reaction).
* Edit file "new_dihedrals_parameters.txt" according to its help file (information of new dihedrals which are formed during the reaction).
* Edit files "existing_bonds.txt", "existing_angles.txt", and "existing_dihedrals.txt" according to their help files (information of 
  existing bonds and constraints, angles, and dihedrals which should be modified after the reaction, in case you have any).
* Edit .mdp files for your simulations. 
  * "martini_em" is for minimization steps.
  * "martini_eq" and "martini_run" are for initial relaxation of the box before starting reactions. In case you want to perform your own 
    designed relaxation steps you can edit "scripts/pre_relax.sh" file.
  * "martini_eqxl" is for a short equilibration step between each loop of reaction.
* Place your itp files of constituents (reagents and solvents) in "data" folder.
## 2. Initial Relaxation
In this step, a single topology file of the whole system is generated and the simulation box (which is consisted of raw materials) is 
equilibrated before switching on the reactions. To this end, you just need to run the file "run_first_relaxation_only.py" in "scripts" 
folder.
## 3. Start the Reaction Loops
In each loop of the reaction, the distance between reacting species is measured and the reaction takes place in case the desired conditions 
(which are specified in inputs) are fulfilled. To this end, you just need to run the file "run_the_loops_only.py" in "scripts" folder.
In case the last loop had been crashed/stopped and you want to resume the loops again, or when you want to resume reactions from some 
previous loops, you need to edit "data/inputs.txt" file and run "run_the_loops_only.py" again.
If you want to do the whole process at once, just run the file "scripts/run_the_whole_process.py" after generating inputs. But it is 
recommended to do steps 2 and then 3, separately. 

# Outputs
Outputs of the reaction process are as follows:

* Folder "min" contains energy minimization files of each loop.
* Folder "md"  contains MD simulation files of each loop.
* Folder "itp" contains itp files of the system in each loop.
* File "conversion.xvg" contains the trend of conversion of the reaction for each reactive bead.
* Files "product.itp" and "topol.top" are the topology files of the system for the last loop.
* The txt files named to your reactive beads, contain the indices of beads that do not react until the current loop.
* File "XL.txt" contains the beads that are located at a specified distance, and so can react.
* File "XL_noprob.txt" contains the "XL.txt" information before applying the probability of the reaction between beads.
* Folder "loops" contain the reactions that take place between bead pairs in each loop. The file "all_loops" contains all the reactions 
  so far.
* Files "undefined_angles.txt" and "undefined_dihedrals" contain the new angles and dihedrals that are formed due to the reactions but 
  the user does not define their parameters in corresponding input files and so they are not added to the topology file.
