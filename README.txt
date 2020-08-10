Project Summary
----------------
This project includes matlab code to simulate element-based tissue growth using the FEBio finite element solver and a python script to simulate element-based tissue growth using ABAQUS CAE. 

These code were first developed as part of a study that compared node-based and element-based approaches.
*add citation once paper is published*


Required Software
-----------------
This program requires the following free software/add-ons for element based modeling:

GIBBON open-source MATLAB add-on: [https://www.gibboncode.org/] 
Gibbon citation: [https://joss.theoj.org/papers/10.21105/joss.00506]

FEBio open-source finite element solver: [https://febio.org/]
FEBio citation: [https://pubmed.ncbi.nlm.nih.gov/22482660/]


How to Use 
-----------
To run the growth simulation, open and run ElementBasedGrowth.m in MATLAB.

The code references an FEBio input geometry file (rudiment.feb) and a function that creates an FEBio log file based on info in this script, and runs the FEBio solver (febio_growth.m).

The program applies growth on an element-by-element basis, as a function of normalized position in the y-direction.

To implement growth, material properties are defined as a solid mixture of cell growth properties (defined by phir, cr, and ce) and neo-Hookean properties (defined by E and v).

The growth function is applied as a change in external concentration (deltCE), which is a function of normalized y-position of the centroid of the element (elecent) and a coefficient of growth (kg1).

Updated geometry (V_growth) and resulting stresses in all elements (E_stress_growth) are reported in output files after each cycle of growth.

Output files save as "tempmodel" in a folder labeled "temp" in the same location as ElementBasedGrowth.m.
