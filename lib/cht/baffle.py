# -*- coding: utf-8 -*-

import os, subprocess
import shutil
from Config import Config
from definitions import *
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import numpy
import gzip

def baffle():
    work = get_work()
    
    config = Config()   
    
    temperature = config.getTemperature()
    temperatureIn = config.getTemperatureIn()
    lowertemp = min([temperature,temperatureIn])     

    for fluid in config.getFluids():
        faceZones_path = os.path.join(work.polyMeshDir(fluid), "faceZones.gz" )
        with gzip.open(faceZones_path, "r") as faceZones_file:
            faceZones = faceZones_file.read()
        
        baffles = []
        for baffle in config.getBaffles():
            if baffle in faceZones:
                config.setBafflesInFluid(baffle, fluid)
                path = os.path.join(work.systemDir(), fluid, "createBafflesDict")
                bafflesDict = ParsedParameterFile(path)
                baffleDict = {
                    "type": "faceZone",
                    "zoneName": baffle,
                    "patches": {
                        "master": {
                            "name":            baffle + "_0",
                            "type":            "mappedWall",
                            "sampleMode":      "nearestPatchFace",
                            "sampleRegion":    fluid,
                            "samplePatch":     baffle + "_1",
                            "offsetMode":      "uniform",
                            "offset":          "(0 0 0)",
                            
                            "patchFields":
                            {
                                "T":
                                {
                                    "type": "compressible::thermalBaffle1D<hConstSolidThermoPhysics>",
                                    "baffleActivated": "yes",
                                    "thickness": "uniform %0.4f" % config.getThickness(baffle),
                                    "Qs": "uniform 0",
                                    "specie":
                                    {
                                        "nMoles": 1,
                                        "molWeight": 12,
                                    },
                                    "transport":
                                    {
                                        "kappa": config.getConductivity(baffle),
                                    },
                                    "thermodynamics":
                                    {
                                        "Hf": 0,
                                        "Cp": 10,
                                    },
                                    "equationOfState":
                                    {
                                        "rho": 8000,
                                    },
                                    "value": "uniform %s" % lowertemp,
                                }
                            }
                        },
                        "slave":
                        {
                            "name":            baffle + "_1",
                            "type":            "mappedWall",
                            "sampleMode":      "nearestPatchFace",
                            "sampleRegion":    fluid,
                            "samplePatch":     baffle + "_0",
                            "offsetMode":      "uniform",
                            "offset":          "(0 0 0)",
                            "patchFields":
                            {
                                "T":
                                {
                                    "type": "compressible::thermalBaffle1D<hConstSolidThermoPhysics>",
                                    "baffleActivated": "yes",
                                    "thickness": "uniform %0.4f" % config.getThickness(baffle),
                                    "Qs": "uniform 0",
                                    "specie":
                                    {
                                        "nMoles": 1,
                                        "molWeight": 12,
                                    },
                                    "transport":
                                    {
                                        "kappa": config.getConductivity(baffle),
                                    },
                                    "thermodynamics":
                                    {
                                        "Hf": 0,
                                        "Cp": 10,
                                    },
                                    "equationOfState":
                                    {
                                        "rho": 8000,
                                    },
                                    "value": "uniform %s" % lowertemp,
                                } 
                            }
                        },
                    },
                }

                
                bafflesDict["baffles"][baffle] = baffleDict
                bafflesDict.writeFile()
                
                baffles.append(baffle)
              
        
        if baffles: 
            config.setBafflesInFluid(baffles, fluid)
            myBasicRunner(["createBaffles", "-overwrite", "-region", fluid], 
                       "createBaffles.%s" % fluid)
                
                
                
#        
#            if fan in boundary:
#                axis = config.getAxis(fan)
#                radius = config.getRadius(fan)
#                extended = extendAxis(axis)
#                point1 = ' '.join([str(x) for x in extended[0]])
#                point2 = ' '.join([str(x) for x in extended[1]])
#                zones.append("cellSet %s new cylinderToCell (%s) (%s) %s" % 
#                             (fan, point1, point2, radius))
#                zones.append("cellZoneSet %s new setToCellZone %s" % (fan, fan))
#                fans.append(fan)
#        
#        if fans:
#            config.setFansInFluid(fans, fluid)
#            
#            setSetFile = os.path.join(work_dir, 
#                                      "createRotorZones.%s.setSet" % fluid)
#            with open(setSetFile, "w") as fobj:
#                fobj.write("\n".join(zones))
#                
#            myBasicRunner(["setSet", "-batch", setSetFile, "-region", fluid], 
#                           "createRotorZones.%s" % fluid)
#            




        
