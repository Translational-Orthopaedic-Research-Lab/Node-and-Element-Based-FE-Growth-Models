# Node-based growth 
# Nikhil Dixit
# MoBL -- NCSU Mechanical Engineering

# This code can be run in ABAQUS CAE to simulate growth using a finite element model.
# Users must open input file M1.cae (containing initial geometry and node sets) in ABAQUS CAE, then copy and paste this code into the ABAQUS command prompt.
# The directory of the input file and resulting output files must be specified in line 35, 123, 185, 188, 209, and 210.
# The input file for this program contains a rudiment geometry named "Humerus," which models a developing long bone. 

from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
p = 1 # growth coefficient
count = 1
mech_hum = 0
mech_scap = 0
bio_hum = 10000
#bio_scap = 5000

for j in range(1,11):
	# Set up model
	mdb.openAuxMdb(pathName=
		'D:\data\temp\M1.cae') # input CAE file with rudiment geometry and node sets 
	mdb.copyAuxMdbModel(fromName='Model-%d' %count, toName='Model-%d' %(count+1)) # names of the new model update for each cycle
	mdb.copyAuxMdbModel(fromName='Model-%d' %count, toName='Model-%d' %(count+1))
	mdb.closeAuxMdb()
    
    # Initial Simulation to establish contact
    # Define material properties
	mdb.models['Model-%d' %count].Material(name='Material-1')
	mdb.models['Model-%d' %count].materials['Material-1'].Density(table=((0.007, ), ))
	mdb.models['Model-%d' %count].materials['Material-1'].Elastic(table=((1000, 0.45), ))
	mdb.models['Model-%d' %count].materials['Material-1'].Expansion(table=((8e-06, ), ))
	mdb.models['Model-%d' %count].HomogeneousSolidSection(material='Material-1', name=
		'Section-1', thickness=None)
	mdb.models['Model-%d' %count].parts['Humerus_%d' %(j-1)].SectionAssignment(offset=0.0, 
		offsetField='', offsetType=MIDDLE_SURFACE, region=
		mdb.models['Model-%d' %count].parts['Humerus_%d' %(j-1)].sets['TOTAL'], sectionName=
		'Section-1', thicknessAssignment=FROM_SECTION)	
    # Apply translation for mechanical simulation    
	#mdb.models['Model-%d' %count].rootAssembly.translate(instanceList=('Humerus_%d-1' %(j-1), ), vector=(-2.0, (-2.0),0.0))
	#if j%2 == 0:
	#	mdb.models['Model-%d' %count].rootAssembly.translate(instanceList=('Humerus_%d-1' %(j-1), ), vector=(-0.0, (0.0),-0.2))
#	if j%6 == 0:
#		mdb.models['Model-%d' %count].rootAssembly.translate(instanceList=('Humerus_%d-1' %(j-1), ), vector=(-0.0, (0.0),-0.2))
	mdb.models['Model-%d' %count].ExplicitDynamicsStep(name='Step-1', previous='Initial')
	mdb.models['Model-%d' %count].OperatorFilter(halt=ON, limit=0.01, name='Filter-1', 
		operation=MAX)
	mdb.models['Model-%d' %count].fieldOutputRequests['F-Output-1'].setValues(filter=
		'Filter-1', variables=('S', ))	
    # Apply Boundary Conditions    
	mdb.models['Model-%d' %count].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
		distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
		'BC-2', region=
		mdb.models['Model-%d' %count].rootAssembly.instances['Humerus_%d-1' %(j-1)].sets['DISP'], 
		u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0)		
    # Run Simulation    
	mdb.Job(activateLoadBalancing=False, atTime=None, contactPrint=OFF, 
		description='', echoPrint=OFF, explicitPrecision=SINGLE, historyPrint=OFF, 
		memory=90, memoryUnits=PERCENTAGE, model='Model-%d' %count, modelPrint=OFF, 
		multiprocessingMode=DEFAULT, name='dyn_%d' %j, nodalOutputPrecision=SINGLE, 
		numCpus=1, numDomains=1, parallelizationMethodExplicit=DOMAIN, queue=None, 
		scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
	#mdb.jobs['dyn_%d' %j].submit(consistencyChecking=OFF)
	#mdb.jobs['dyn_%d' %j].waitForCompletion() 
    
    # Mechanical simulation to measure stress
    # Define material properties
	mdb.models['Model-%d' %(count+1)].Material(name='Material-1')
	mdb.models['Model-%d' %(count+1)].materials['Material-1'].Density(table=((0.007, ), ))
	mdb.models['Model-%d' %(count+1)].materials['Material-1'].Elastic(table=((1000, 0.45), ))
	mdb.models['Model-%d' %(count+1)].materials['Material-1'].Expansion(table=((8e-06, ), ))
	mdb.models['Model-%d' %(count+1)].HomogeneousSolidSection(material='Material-1', name=
		'Section-1', thickness=None)
	mdb.models['Model-%d' %(count+1)].parts['Humerus_%d' %(j-1)].SectionAssignment(offset=0.0, 
		offsetField='', offsetType=MIDDLE_SURFACE, region=
		mdb.models['Model-%d' %(count+1)].parts['Humerus_%d' %(j-1)].sets['TOTAL'], sectionName=
		'Section-1', thicknessAssignment=FROM_SECTION)
	mdb.models['Model-%d' %(count+1)].rootAssembly.DatumCsysByDefault(CARTESIAN)
    #
	#mdb.models['Model-%d' %(count+1)].rootAssembly.translate(instanceList=('Humerus_%d-1' %(j-1), ), vector=(-(j+0.5), (-(j+0.5)), 0.0))
	#mdb.models['Model-%d' %(count+1)].rootAssembly.translate(instanceList=('Humerus_%d-1' %(j-1), ), vector=(-(0.5), (-(0.5)), 0.0))
	#if j%2 == 0:
	#	mdb.models['Model-%d' %(count+1)].rootAssembly.translate(instanceList=('Humerus_%d-1' %(j-1), ), vector=(-0.0, (0.0),-0.2))
#	if j%6 == 0:
#		mdb.models['Model-%d' %(count+1)].rootAssembly.translate(instanceList=('Humerus_%d-1' %(j-1), ), vector=(-0.0, (0.0),-0.2))
	#dist_x = ((mdb.models['Model-%d' %(count+1)].rootAssembly.instances['Scapula_%d-1' %(j-1)].nodes[min_nod_sc-1].coordinates[0]) - (mdb.models['Model-%d' %(count+1)].rootAssembly.instances['Humerus_%d-1' %(j-1)].nodes[min_nod-1].coordinates[0]))
	#dist_y = ((mdb.models['Model-%d' %(count+1)].rootAssembly.instances['Scapula_%d-1' %(j-1)].nodes[min_nod_sc-1].coordinates[1]) - (mdb.models['Model-%d' %(count+1)].rootAssembly.instances['Humerus_%d-1' %(j-1)].nodes[min_nod-1].coordinates[1]))
	#mdb.models['Model-%d' %(count+1)].rootAssembly.translate(instanceList=('Humerus_%d-1' %(j-1), ), vector=(-(dist_x*2), -(dist_y*2), 0))
	mdb.models['Model-%d' %(count+1)].StaticStep(initialInc=1.0, maxNumInc=1000, 
		name='Step-1', nlgeom=ON, previous='Initial')
	mdb.models['Model-%d' %(count+1)].fieldOutputRequests['F-Output-1'].setValues(variables=(
		'PRESSONLY', 'U'))
 #from muscle scaling opensim simulation a compressive force of 235 N was found. Joint stiffness of 0.0005N/mm was assumed for the simulation. 		
	pos = 0 
	pos_m = [0] * 1
	n = 0
	import string
	mdb.models['Model-%d' %(count+1)].keywordBlock.synchVersions()
	for block in mdb.models['Model-%d' %(count+1)].keywordBlock.sieBlocks:
		if string.lower(block[0:len('*Output, field')])==string.lower('*Output, field'):
			pos_m[n] = pos
			n = n+1
		pos = pos +1 
	mdb.models['Model-%d' %(count+1)].keywordBlock.replace(pos_m[0] + 2, """
	*Element Output,POSITION= NODES, directions=YES
	PRESSONLY
	""")
	mdb.save()
    # Run Simulation
	mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
		explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
		memory=90, memoryUnits=PERCENTAGE, model='Model-%d' %(count+1), modelPrint=OFF, 
		multiprocessingMode=DEFAULT, name='static_%d' %j, nodalOutputPrecision=SINGLE, 
		numCpus=8, numDomains=8, numGPUs=0, queue=None, scratch='', type=ANALYSIS, 
		userSubroutine='', waitHours=0, waitMinutes=0)
	#mdb.jobs['static_%d' %j].submit(consistencyChecking=OFF)
	#mdb.jobs['static_%d' %j].waitForCompletion() 
	# Importing the stress analysis cae model 
	mdb.openAuxMdb(pathName=
		'D:\data\temp\M1.cae')
	mdb.copyAuxMdbModel(fromName='Model-%d' %(count+1), toName='Model-%d' %(count+3)) # names of the new model 
	mdb.copyAuxMdbModel(fromName='Model-%d' %(count+1), toName='Model-%d' %(count+3))
	mdb.closeAuxMdb()
    
    # Simulate Growth
	#mdb.models['Model-%d' %(count+3)].boundaryConditions['BC-2'].setValues(u1=0.0)
	#mdb.models['Model-%d' %(count+3)].boundaryConditions['BC-2'].setValues(u2=0.0)
	#mdb.models['Model-%d' %(count+3)].interactions['Int-1'].suppress()
    # Define growth stimulus as a function of y-position
	mdb.models['Model-%d' %(count+3)].rootAssembly.DatumCsysByThreePoints(coordSysType=
		CARTESIAN, name='HUm_cs', origin= mdb.models['Model-%d' %(count+3)].rootAssembly.instances['Humerus_%d-1' %(j-1)].nodes[218].coordinates, point1= mdb.models['Model-%d' %(count+3)].rootAssembly.instances['Humerus_%d-1' %(j-1)].nodes[183].coordinates, 
		point2= mdb.models['Model-%d' %(count+3)].rootAssembly.instances['Humerus_%d-1' %(j-1)].nodes[814].coordinates)	
	y_hum = sqrt((((mdb.models['Model-%d' %(count+3)].rootAssembly.instances['Humerus_%d-1' %(j-1)].nodes[218].coordinates[0]) - (mdb.models['Model-%d' %(count+3)].rootAssembly.instances['Humerus_%d-1' %(j-1)].nodes[814].coordinates[0])) **2) + 
		(((mdb.models['Model-%d' %(count+3)].rootAssembly.instances['Humerus_%d-1' %(j-1)].nodes[218].coordinates[1]) - (mdb.models['Model-%d' %(count+3)].rootAssembly.instances['Humerus_%d-1' %(j-1)].nodes[814].coordinates[1]))**2) + 
		(((mdb.models['Model-%d' %(count+3)].rootAssembly.instances['Humerus_%d-1' %(j-1)].nodes[218].coordinates[2]) - (mdb.models['Model-%d' %(count+3)].rootAssembly.instances['Humerus_%d-1' %(j-1)].nodes[814].coordinates[2]))**2))
	mdb.models['Model-%d' %(count+3)].ExpressionField(description='', expression=
		'(Y/y_hum)**p'
		, localCsys=mdb.models['Model-%d' %(count+3)].rootAssembly.datums[mdb.models['Model-%d' %(count+3)].rootAssembly.features['HUm_cs'].id], name=
		'AnalyticalField-1')
    # Apply growth stimulus as temperature to induce thermal expansion    
	mdb.models['Model-%d' %(count+3)].Temperature(createStepName='Step-1', 
		crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=FIELD
		, field='AnalyticalField-1', magnitudes=(bio_hum, ), name='Hum_temp', region=
		mdb.models['Model-%d' %(count+3)].rootAssembly.instances['Humerus_%d-1' %(j-1)].sets['TOTAL'])
	mdb.models['Model-%d' %(count+3)].TabularAmplitude(data=((0.0, 0.0), (1.0, 1.0)), name=
    'Amp-1', smooth=SOLVER_DEFAULT, timeSpan=STEP)
	mdb.models['Model-%d' %(count+3)].predefinedFields['Hum_temp'].setValues(amplitude='Amp-1')
    # Apply Boundary Conditions
    # Fix bottom nodes (DISP) in the y-direction
	mdb.models['Model-%d' %(count+3)].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
		distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
		'BC-2', region=
		mdb.models['Model-%d' %(count+3)].rootAssembly.instances['Humerus_%d-1' %(j-1)].sets['DISP'], 
		u1=UNSET, u2=0.0, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)	
    # Fix top node (TOP) in the x and z-directions
	mdb.models['Model-%d' %(count+3)].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
		distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
		'BC-3', region=
		mdb.models['Model-%d' %(count+3)].rootAssembly.instances['Humerus_%d-1' %(j-1)].sets['TOP'], 
		u1=0.0, u2=UNSET, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET)	
	#mdb.models['Model-%d' %(count+3)].Temperature(amplitude='Amp-1', createStepName='Step-1', 
	#	crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
	#	UNIFORM, magnitudes=(bio_hum, ), name='Hum_temp', region=
	#	mdb.models['Model-%d' %(count+3)].rootAssembly.instances['Humerus_%d-1' %(j-1)].sets['GROWTH'])	
	#mdb.models['Model-%d' %(count+3)].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
	#	distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
	#	'BC-2', region=
	#	mdb.models['Model-%d' %(count+3)].rootAssembly.instances['Humerus_%d-1' %(j-1)].sets['DISP'], 
	#	u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0)	
	#mdb.models['Model-%d' %(count+3)].ExpressionField(description='', expression=
	#	'(11000*(0.14 -(0.87*((-Z/3.0)**1))+(4.4*((-Z/3.0)**2))-(2.66*((-Z/3.0)**3))))'
	#	, localCsys=mdb.models['Model-%d' %(count+3)].rootAssembly.datums[mdb.models['Model-%d' %(count+3)].rootAssembly.features['scap_cs'].id], name=
	#	'AnalyticalField-2')
	#mdb.models['Model-%d' %(count+3)].Temperature(createStepName='Step-1', 
	#	crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=FIELD
	#	, field='AnalyticalField-2', magnitudes=(0.02, ), name='Scap_temp', region=
	#	mdb.models['Model-%d' %(count+3)].rootAssembly.instances['Scapula_%d-1' %(j-1)].sets['TOTAL'])
    # Run Simulation
	mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
		explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
		memory=90, memoryUnits=PERCENTAGE, model='Model-%d' %(count+3), modelPrint=OFF, 
		multiprocessingMode=DEFAULT, name='Biogrowth_%d' %j, nodalOutputPrecision=SINGLE, 
		numCpus=8, numDomains=8, numGPUs=0, queue=None, scratch='', type=ANALYSIS, 
		userSubroutine='', waitHours=0, waitMinutes=0)
	mdb.jobs['Biogrowth_%d' %j].submit(consistencyChecking=OFF)
	mdb.jobs['Biogrowth_%d' %j].waitForCompletion() 
    
    # Final deformed model after growth
	mdb.Model(modelType=STANDARD_EXPLICIT, name='Model-%d' %(count+4))
	mdb.models['Model-%d' %(count+4)].PartFromOdb(instance='HUMERUS_%d-1' %(j-1), name='Humerus_%d' %(j-1), 
		odb=session.openOdb(
		r'D:\data\temp\Biogrowth_%d.odb' %j))
	mdb.models['Model-%d' %(count+4)].PartFromOdb(frame=-1, instance='HUMERUS_%d-1' %(j-1), name='Humerus_%d' %j, 
		odb=session.openOdb(
		r'D:\data\temp\Biogrowth_%d.odb' %j), 
		shape=DEFORMED, step=0)
	# Prepare for next cycle
	count = count+4
	mdb.Model(name='Model-%d' %(count+1), objectToCopy=mdb.models['Model-%d' %count])
	#mdb.Model(name='Model-%d' %(count+2), objectToCopy=mdb.models['Model-%d' %count])
	mdb.models['Model-%d' %count].Material(name='Material-1')
	mdb.models['Model-%d' %count].materials['Material-1'].Density(table=((0.007, ), ))
	mdb.models['Model-%d' %count].materials['Material-1'].Elastic(table=((1.1, 0.45), ))
	mdb.models['Model-%d' %count].materials['Material-1'].Expansion(table=((8e-06, ), ))
	mdb.models['Model-%d' %count].HomogeneousSolidSection(material='Material-1', name=
		'Section-1', thickness=None)
	mdb.models['Model-%d' %count].parts['Humerus_%d' %j].SectionAssignment(offset=0.0, 
		offsetField='', offsetType=MIDDLE_SURFACE, region=
		mdb.models['Model-%d' %count].parts['Humerus_%d' %j].sets['TOTAL'], sectionName=
		'Section-1', thicknessAssignment=FROM_SECTION)	
	mdb.models['Model-%d' %count].rootAssembly.Instance(dependent=ON, name='Humerus_%d-1' %j, 
		part=mdb.models['Model-%d' %count].parts['Humerus_%d' %j])
	#mdb.models['Model-%d' %count].rootAssembly.translate(instanceList=('Humerus_%d-1' %j, ), vector=((j+0.5), (j+0.5),0.0))
	#mdb.models['Model-%d' %count].rootAssembly.translate(instanceList=('Humerus_%d-1' %j, ), vector=((0.5), (0.5),0.0))
	# Save output data
    mdb.save()
	mdb.saveAs(pathName='D:\data\temp\M1_%d.cae' %j)
	mdb.saveAs(pathName='D:\data\temp\M1.cae')