%% %% This file creates runs FEBio using node displacements as boundary conditions.
%% Allows control of each node and assignment of element-specific material properties.
%% Structure partially modified from Gibbon: DEMO_spatially_varying_material_parameters

function [dispnodes,E_stress,Volume]=febio_growth(febinfo,febgeo,febmat)

%FEB Info
FEB_struct.febio_spec.version=febinfo.version;
FEB_struct.Module.Type=febinfo.module;
FEB_struct.run_filename=febinfo.febname; %FEB file name
FEB_struct.run_logname=febinfo.logname; %FEBio log file name

FEB_struct.Control.AnalysisType=febinfo.Control.AnalysisType;
FEB_struct.Control.Properties=febinfo.Control.Properties;
FEB_struct.Control.Values=febinfo.Control.Values;
FEB_struct.Control.TimeStepperProperties=febinfo.Control.TimeStepperProperties;
FEB_struct.Control.TimeStepperValues=febinfo.Control.TimeStepperValues;

FEB_struct.Globals.Constants.Names=febinfo.Globals.Constants.Names;
FEB_struct.Globals.Constants.Entries=febinfo.Globals.Constants.Entries;

%Creating FEB Geometry
FEB_struct.Geometry.Nodes=febgeo.Geometry.Nodes;
FEB_struct.Geometry.Elements=febgeo.Geometry.Elements; %The element sets
FEB_struct.Geometry.ElementType=febgeo.Geometry.ElementType; %The element types
FEB_struct.Geometry.ElementMat=febgeo.Geometry.ElementMat;
FEB_struct.Geometry.ElementsPartName=febgeo.Geometry.ElementsPartName;

FEB_struct.Geometry.NodeSet{1}.Set=febgeo.Geometry.NodeSet{1}.Set;
FEB_struct.Geometry.NodeSet{1}.Name=febgeo.Geometry.NodeSet{1}.Name;
FEB_struct.Geometry.NodeSet{2}.Set=febgeo.Geometry.NodeSet{2}.Set;
FEB_struct.Geometry.NodeSet{2}.Name=febgeo.Geometry.NodeSet{2}.Name;

% DEFINING SPATIALLY VARYING MATERIAL SET
for q=1:1:length(febmat.Materials)
    FEB_struct.Materials{q}.Type=febmat.Materials{q}.Type;
    FEB_struct.Materials{q}.Solid{1}.Type=febmat.Materials{q}.Solid{1}.Type;
    FEB_struct.Materials{q}.Solid{1}.Properties=febmat.Materials{q}.Solid{1}.Properties;
    FEB_struct.Materials{q}.Solid{1}.Values=febmat.Materials{q}.Solid{1}.Values;

    FEB_struct.Materials{q}.Solid{2}.Type=febmat.Materials{q}.Solid{2}.Type;
    FEB_struct.Materials{q}.Solid{2}.Properties=febmat.Materials{q}.Solid{2}.Properties;
    FEB_struct.Materials{q}.Solid{2}.Values=febmat.Materials{q}.Solid{2}.Values;
    FEB_struct.Materials{q}.Solid{2}.PropAttrName=febmat.Materials{q}.Solid{2}.PropAttrName;
    FEB_struct.Materials{q}.Solid{2}.PropAttrVal=febmat.Materials{q}.Solid{2}.PropAttrVal;
    
end

%Adding BC information

    FEB_struct.Boundary.Fix{1}.bc='y';
    FEB_struct.Boundary.Fix{1}.SetName=FEB_struct.Geometry.NodeSet{1}.Name;
    FEB_struct.Boundary.Fix{2}.bc='x';
    FEB_struct.Boundary.Fix{2}.SetName=FEB_struct.Geometry.NodeSet{2}.Name;
    FEB_struct.Boundary.Fix{3}.bc='z';
    FEB_struct.Boundary.Fix{3}.SetName=FEB_struct.Geometry.NodeSet{2}.Name;
    
%Load curves for CE
for q=1:1:length(febmat.Materials)
    FEB_struct.LoadData.LoadCurves.id(q)=febmat.LoadData.LoadCurves.id(q);
    FEB_struct.LoadData.LoadCurves.type{q}=febmat.LoadData.LoadCurves.type{q};
    FEB_struct.LoadData.LoadCurves.loadPoints{q}=febmat.LoadData.LoadCurves.loadPoints{q};
end
    
%Adding output requests
FEB_struct.Output.VarTypes={'displacement','stress','relative volume'};

%Specify log file output
run_disp_output_name=[FEB_struct.run_filename(1:end-4),'_node_out.txt'];
run_force_output_name=[FEB_struct.run_filename(1:end-4),'_force_out.txt'];
run_stress_output_name=[FEB_struct.run_filename(1:end-4),'_stress_out.txt'];
run_volume_output_name=[FEB_struct.run_filename(1:end-4),'_volume_out.txt'];
FEB_struct.run_output_names={run_disp_output_name,run_force_output_name,run_stress_output_name,run_volume_output_name};
FEB_struct.output_types={'node_data','node_data','element_data','element_data'};
FEB_struct.data_types={'ux;uy;uz','Rx;Ry;Rz','sx;sy;sz;sxy;syz;sxz','J'};

%% SAVING .FEB FILE  %Based on febStructfebFile.m in Gibbon

FEB_struct.disp_opt=0; %Display waitbars
dispStartTitleGibbonCode('Writing FEBio XML object');
if ~isfield(FEB_struct,'disp_opt')
    FEB_struct.disp_opt=0;
end
docNode = com.mathworks.xml.XMLUtils.createDocument('febio_spec'); %Create the overall febio_spec field

%Set febio_spec
febio_spec = docNode.getDocumentElement;
if ~isfield(FEB_struct,'febio_spec')
    FEB_struct.febio_spec.version='2.0';
elseif ~isfield(FEB_struct.febio_spec,'version')
    FEB_struct.febio_spec.version='2.0';
end
febio_spec.setAttribute('version',FEB_struct.febio_spec.version); %Adding version attribute

% Add comment if present
if isfield(FEB_struct,'commentField')
    commentString = FEB_struct.commentField;
else %Default comment
    commentString = ['Created using GIBBON, ',datestr(now)];
end
commentNode = docNode.createComment(commentString);
febio_spec.appendChild(commentNode);

% DEFINING MODULE LEVEL
if ~isfield(FEB_struct,'Module')
    FEB_struct.Module.Type='solid'; %Use solid as default module
end
docNode=addModuleLevel_FEB(docNode,FEB_struct);

% DEFINE CONTROL SECTION
if isfield(FEB_struct,'Control')
    docNode=addControlLevel_FEB(docNode,FEB_struct);
end

% DEFINING GLOBALS LEVEL
docNode=addGlobalsLevel_FEB(docNode,FEB_struct);

% DEFINING MATERIAL LEVEL
docNode=addMaterialLevel_FEB(docNode,FEB_struct);

% DEFINING GEOMETRY LEVEL
writeMethod=1;
switch writeMethod
    case 1 % TEXT FILE PARSING (faster for large arrays)
        docNode=addGeometryLevel_TXT(docNode,FEB_struct);
    case 2 %XML PARSING
        docNode=addGeometryLevel_FEB(docNode,FEB_struct);
end

% DEFINE BOUNDARY CONDITIONS LEVEL AND LOADS LEVEL
if isfield(FEB_struct,'Boundary')
    [docNode]=addBoundaryLevel_FEB(docNode,FEB_struct);
end

% DEFINE CONSTRAINTS LEVEL
if isfield(FEB_struct,'Constraints')
    [docNode]=addConstraintsLevel_FEB(docNode,FEB_struct);
end

% DEFINE LOADDATA LEVEL
%if isfield(FEB_struct,'LoadData')
[docNode]=addLoadDataLevel_FEB(docNode,FEB_struct);
%end

% DEFINE OUTPUT LEVEL
docNode=addOutputLevel_FEB(docNode,FEB_struct);

% CREATE OUTPUT OR EXPORT XML FILE

exportFEB_XML(FEB_struct.run_filename,docNode)
% switch nargout
%     case 0
%         disp('Writing .feb file');
%         if isfield(FEB_struct,'topCommentLine')
%             exportFEB_XML(FEB_struct.run_filename,docNode,FEB_struct.topCommentLine); % Saving XML file
%         else
%             exportFEB_XML(FEB_struct.run_filename,docNode); % Saving XML file
%         end
%     case 1
         varargout{1}=docNode;
% end
dispDoneGibbonCode;

%% RUNNING FEBIO JOB

% FEBioRunStruct.FEBioPath='C:\Program Files\febio2-2.2.6\bin\FEBio2.exe';
% FEBioRunStruct.FEBioPath='/Applications/FEBio2.5.2/bin/FEBio2.exe';
FEBioRunStruct.run_filename=FEB_struct.run_filename;
FEBioRunStruct.run_logname=FEB_struct.run_logname;
FEBioRunStruct.disp_on=1;
FEBioRunStruct.disp_log_on=1;
FEBioRunStruct.runMode='external';%'internal';
FEBioRunStruct.t_check=0.5; %Time for checking log file (dont set too small)
FEBioRunStruct.maxtpi=1e99; %Max analysis time
FEBioRunStruct.maxLogCheckTime=30; %Max log file checking time

[runFlag]=runMonitorFEBio(FEBioRunStruct);%START FEBio NOW!!!!!!!!

%% IMPORTING NODAL DISPLACEMENT RESULTS
% Importing nodal displacements from a log file
[~, N_disp_mat,~]=importFEBio_logfile(FEB_struct.run_output_names{1}); %Nodal displacements
[~, E_stress,~]=importFEBio_logfile(FEB_struct.run_output_names{3}); %Element stresses
[~, Volume,~]=importFEBio_logfile(FEB_struct.run_output_names{4}); %Element volume

dispnodes=N_disp_mat(:,2:end,end);%Final nodal displacements
E_stress=E_stress(:,:,end);
Volume=Volume(:,:,end);

