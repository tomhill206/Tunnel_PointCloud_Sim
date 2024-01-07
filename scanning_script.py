import bpy
import range_scanner

# Edit path to csv to match your own
output_path = "/Users/tomhill/Documents/Tunnel_PointCloud_Sim/data/csv/"

file_name = 'tunnel'
step_degree = 0.3

# Velodyne
range_scanner.ui.user_interface.scan_rotating(
    bpy.context, 

    scannerObject=bpy.context.scene.objects["Scanner"],

    xStepDegree=step_degree, fovX=360.0, yStepDegree=step_degree, fovY=180.0, rotationsPerSecond=20,

    reflectivityLower=0.0, distanceLower=0.0, reflectivityUpper=0.0, distanceUpper=99999.9, maxReflectionDepth=10,
    
    enableAnimation=False, frameStart=1, frameEnd=1, frameStep=1, frameRate=1,

    addNoise=True, noiseType='gaussian', mu=0.0, sigma=0.01, noiseAbsoluteOffset=0.0, noiseRelativeOffset=0.0, 

    simulateRain=False, rainfallRate=0.0, 

    addMesh=True,

    exportLAS=False, exportHDF=False, exportCSV=True, exportPLY=False, exportSingleFrames=False,
    dataFilePath=output_path, dataFileName=file_name,
    
    debugLines=False, debugOutput=False, outputProgress=False, measureTime=False, singleRay=False, destinationObject=None, targetObject=None
)  
