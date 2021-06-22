Project Summary
----------------
This project includes Matlab code to simulate element-based tissue growth using the FEBio finite element solver and a python script to simulate element-based tissue growth using ABAQUS CAE. 

These code were developed as part of a study that compared node-based and element-based approaches.


Required Software
-----------------
This program requires the following free software/add-ons for element-based simulations:

FEBio open-source finite element solver: [https://febio.org/]
FEBio citation: [https://pubmed.ncbi.nlm.nih.gov/22482660/]

GIBBON open-source MATLAB add-on: [https://www.gibboncode.org/] 
Gibbon citation: [https://joss.theoj.org/papers/10.21105/joss.00506]

This program requires the following commercial software for node-based simulations:

ABAQUS CAE: [https://www.3ds.com/products-services/simulia/products/abaqus/abaquscae/]


How to Use 
-----------

FEBIO (Element-based approach)
------------------------------
To run the element-based growth simulation, open and run ElementBasedGrowth.m in MATLAB.

The code references an FEBio input geometry file (rudiment.feb) and a function that creates an FEBio log file based on info in this script, and runs the FEBio solver (febio_growth.m).

The program applies growth on an element-by-element basis, as a function of normalized position in the y-direction.

To implement growth, material properties are defined as a solid mixture of cell growth properties (defined by phir, cr, and ce) and neo-Hookean properties (defined by E and v).

The growth function is applied as a change in external concentration (deltCE), which is a function of normalized y-position of the centroid of the element (elecent) and a coefficient of growth (kg1).

Updated geometry (V_growth) and resulting stresses in all elements (E_stress_growth) are reported in output files after each cycle of growth.

Output files save as "tempmodel" in a folder labeled "temp" in the same location as ElementBasedGrowth.m.

ABAQUS (Node-based approach)
------------------------------
To run the node-based growth simulation, open the initial ABAQUS CAE file (M1.cae) containing the initial geometry and mesh.

Copy and paste the python script (NodeBasedGrowth.py) into the command line in ABAQUS and press enter twice to run.

The program applies expansion between nodes, as a function of normalized position in the y-direction.

Growth is achieved using thermal expansion capabilitys, where the growth function is applied as a temperature differential, as a function of normalized y-position of each node.

Output files containing results are produced after each cycle.
