%% Spatially varying element-based growth
% Danielle Howe
% TORL -- UNC/NCSU BME

% This file imports a rudiment geometry (rudiment.feb) and then runs FEBio 
% to control element-specific growth.

% This program applies growth on an element-by-element basis, as a function 
% of normalized position in the y-direction.

% Structure modified from Gibbon: DEMO_spatially_varying_material_parameters

% This code relies on the following matlab function: febio_growth.m 

%%
clear; close all; clc;
%%
% path names to find part
defaultFolder = fileparts(mfilename('fullpath'));
% path to save output files
savePath=fullfile(defaultFolder,'temp');
% output file name
modelName=fullfile(savePath,'tempmodel');

%Import Rudiment Geometry- tet4 mesh
[febXML,nodeStruct,elementCell]=import_FEB('rudiment.feb');

V=nodeStruct.N; % Define nodes
E=elementCell{1}.E; % Define elements

%% BUILD MODEL
elementMaterialIndices=[1:1:length(E(:,1))]';
numel=length(E(:,1));

% SET UP BOUNDARY CONDITIONS
% Establish node sets to fix
logicBottomNodes=zeros(length(V(:,3)),1);
logicBottomNodes(1,1)=1;
if exist('logicBottomNodes','var')>0
bcFixList=find(logicBottomNodes);
end

% Nodes at the base to be fixed in y-direction
bcFixList=find(V(:,2)==0); 
% Nodes along the y-axis to be fixed in x-,z-directions
bcFixList2=[find(abs(V(:,3))<0.0000001 & abs(V(:,1))<0.0000001)]; 

% FEB Model Info
febinfo.febname=[modelName,'.feb']; %FEB file name
febinfo.logname=[modelName,'.log']; %FEBio log file name
febinfo.version='2.0';
febinfo.module='solid';

% Control section
febinfo.Control.AnalysisType='static';
febinfo.Control.Properties={'time_steps','step_size',...
    'max_refs','max_ups',...
    'dtol','etol','rtol','lstol'};
febinfo.Control.Values={10,0.1,...
    15,0,...
    0.001,0.01,0,0.9};
febinfo.Control.TimeStepperProperties={'dtmin','dtmax','max_retries','opt_iter','aggressiveness'};
febinfo.Control.TimeStepperValues={1e-5,0.1,10,10,1};
febinfo.Globals.Constants.Names={'T','R','Fc'};
febinfo.Globals.Constants.Entries={298,8.314e-06,0};

% FEB Geometry
febgeo.Geometry.Nodes=V;
febgeo.Geometry.Elements={E}; %The element sets
febgeo.Geometry.ElementType={'tet4'}; %The element types
febgeo.Geometry.ElementMat={elementMaterialIndices};
febgeo.Geometry.ElementsPartName={'Block'};

% Define node sets
if exist('logicBottomNodes','var')>0
    febgeo.Geometry.NodeSet{1}.Set=bcFixList;
    febgeo.Geometry.NodeSet{1}.Name='bcFixList';
    febgeo.Geometry.NodeSet{2}.Set=bcFixList2;
    febgeo.Geometry.NodeSet{2}.Name='bcFixList2';
end

%% Multi-step Growth

% Define growth parameters
gsteps=10; % Number of growth cycles
kg1=0.24; % Element-based growth coefficient
% kg2=-0.87;
% kg3=4.4;
% kg4=-2.66;
% kg5=0.14;
e=0.001; % elastic modulus in MPa
v=0.49; % poisson's ratio
phir=0.000001; % phi value

CR=zeros(numel,gsteps);
CR2=zeros(numel,gsteps);
CE=zeros(numel,gsteps);
V_growth=zeros(length(V(:,1)),length(V(1,:)),gsteps+1);
V_growth(:,:,1)=V; 
E_stress_growth=zeros(numel,7,gsteps+1);
Vol_growth=zeros(numel,2,gsteps+1);
Vol_growth(:,:,1)=1;
elecent=zeros(numel,1);

for k=1:gsteps
% Define element y-centroid of each element
elecenttemp=zeros(numel,1);
for x=1:1:numel
    currleng=max(V_growth(:,2,k)); 
    % prescribe "temperature" for expansion based on y-centroid normalized
    % to rudiment height
    elecenttemp(x)=mean([V_growth(E(x,1),2,k),V_growth(E(x,2),2,k),V_growth(E(x,3),2,k),V_growth(E(x,4),2,k)])/currleng;
    if elecenttemp(x)>0
        elecent(x)=elecenttemp(x);
    else
        elecent(x)=elecent(x);
    end
end
    
% Define Cell Growth Model- Load from CR to CR2
deltCE=kg1*elecent; % linear function of normalized y-centroid
% deltCE=kg1*(kg5+kg2*elecent+kg3*elecent.^2+kg4*elecent.^3);
CR(:,k)=200;
CE(:,k)=CR(:,k)/(1-phir);
CR2(:,k)=CE(:,k).*(deltCE+1-phir);

%Define current geometry
febgeo.Geometry.Nodes=V_growth(:,:,k);

for q=1:1:numel      
    %Defining material parameters
    febmat.Materials{q}.Type='solid mixture';
    febmat.Materials{q}.Solid{1}.Type='neo-Hookean';
    febmat.Materials{q}.Solid{1}.Properties={'E','v'};
    febmat.Materials{q}.Solid{1}.Values={e,v};

    febmat.Materials{q}.Solid{2}.Type='cell growth';
    febmat.Materials{q}.Solid{2}.Properties={'phir','cr','ce'};
    febmat.Materials{q}.Solid{2}.Values={phir,1,CE(q,k)};
    febmat.Materials{q}.Solid{2}.PropAttrName={[],'lc',[]};
    febmat.Materials{q}.Solid{2}.PropAttrVal={[],q,[]};
    
    febmat.LoadData.LoadCurves.id(q)=q;
    febmat.LoadData.LoadCurves.type{q}={'linear'};
    febmat.LoadData.LoadCurves.loadPoints{q}=[0 CR(q,k);1 CR2(q,k)];
end

% run FEBio through febio_growth function 
[dispnodes,E_stress,Volume]=febio_growth(febinfo,febgeo,febmat);
V_def=V_growth(:,:,k)+dispnodes; % deformed node positions 
V_growth(:,:,k+1)=V_def; % update geometry 
E_stress_growth(:,:,k+1)=E_stress; % elemental stresses
Vol_growth(:,:,k+1)=Volume; 

% CREATING NODE SET IN DEFORMED STATE

DN_magnitude=sqrt(sum(dispnodes.^2,2));

% Print cycle number
fprintf(2, 'Completed cycle %d\n', k);
end



