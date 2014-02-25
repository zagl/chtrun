# -*- coding: utf-8 -*-

import os, subprocess
import shutil
from ..Config import Config
from ..definitions import *
from fan import fan

def split():
    work = get_work()
    
    config = Config()

    geoms = config.getSolids()

    def getCellSets():
        cellSets = []
        sets = subprocess.Popen(["echo '' | setSet -latestTime -case " + work_dir], 
                                stdout=subprocess.PIPE, shell=True)
        for line in sets.stdout.readlines():
            if "cellZones:" in line:
                break
            if "region" in line:
                name = line.split()[0]
                cells = int(line.split(":")[1])
                cellSets.append({"name": name, "cells": cells})
        return cellSets

    
    print "Running checkMesh"
    check = subprocess.Popen(["checkMesh -case " + work_dir + " | grep cells:"], 
                            stdout=subprocess.PIPE, shell=True)
    meshSize = int(check.stdout.readlines()[0].split(":")[1].strip())


    myBasicRunner(["splitMeshRegions", "-cellZones", "-makeCellZones", 
                   "-overwrite"], "first")
    mergeSolidsPath = os.path.join(work_dir, "mergeSolids.setSet")
    with open(mergeSolidsPath, "w") as fobj:
        for cellSet in getCellSets():
            name = cellSet["name"]
            for geom in geoms:
                fobj.write("cellSet %s delete zoneToCell %s\n" % (name, geom))
                
    myBasicRunner(["setSet", "-batch", mergeSolidsPath], "mergeSolids")

    fluids = []
    fluidNr = 1
    cellsRegionExists = False
    createFluidsPath = os.path.join(work_dir, "createFluids.setSet")
    with open(createFluidsPath, "w") as fobj:
        fobj.write("cellSet cells new\n")
        for cellSet in getCellSets():
            cells = cellSet["cells"]
            name = cellSet["name"]
            if cells > 0.02 * meshSize:
                fluid = "FLUID%d" % fluidNr
                fluids.append(fluid)
                fluidNr += 1
                fobj.write("cellSet %s new cellToCell %s\n" % (fluid, name)) 
                fobj.write("cellZoneSet %s new setToCellZone %s\n" % 
                           (fluid, fluid))
                for folder in ["constant", "system"]:
                    fluidDir = os.path.join("run", folder, fluid)
                    template = os.path.join(region_template_dir, folder, "FLUID")
                    if not os.path.exists(os.path.join(folder, fluid)):
                        shutil.copytree(template, fluidDir)
                config.addFluid(fluid)
            elif cells != 0:
                fobj.write("cellSet cells add cellToCell %s\n" % name) 
                cellsRegionExists = True
            fobj.write("cellSet %s remove\n" % name)
            fobj.write("cellZoneSet %s remove\n" % name)
        
        if cellsRegionExists:
            for geom in geoms:
                fobj.write("cellSet cells delete zoneToCell %s\n" % geom)
            fobj.write("cellSet cells invert\n")
        else:
            fobj.write("cellSet cells remove\n")

#        if cellsRegionExists:
#            for geom in geoms:
#                fobj.write("cellSet cells delete zoneToCell %s\n" % geom)
#        fobj.write("cellSet cells add nbrToCell 2\n")
#        fobj.write("cellSet cells invert\n")

    myBasicRunner(["setSet", "-batch", createFluidsPath], "createFluids")
    
    if cellsRegionExists:
        myBasicRunner(["subsetMesh", "cells", "-overwrite"])

    myBasicRunner(["splitMeshRegions", "-cellZonesOnly", "-overwrite"], "second")
    
    myBasicRunner(["paraFoam", "-touchAll"])
    
#    for fluid in fluids:
#        createFluidsPath = os.path.join(work_dir, "removeCells%s.setSet" % fluid)
#        with open(createFluidsPath, "w") as fobj:
#            fobj.write("cellSet c0 new nbrToCell 2\n")
#            fobj.write("cellSet c0 invert\n")
#        myBasicRunner(["setSet", "-batch", createFluidsPath, "-region", fluid], "removeCells%s" % fluid)
#        myBasicRunner(["subsetMesh", "c0", "-overwrite", "-region", fluid], "%s" % fluid)

    for oldFluid in config.getFluids():
        if oldFluid not in fluids:
            config.rmFluid(oldFluid)
    



        
        
