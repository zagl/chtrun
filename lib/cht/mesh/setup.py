# -*- coding: utf-8 -*-

import os, subprocess, math, re
from ..Config import Config
from ..definitions import *
from Snappy import Snappy
from Feature import Feature
from PyFoam.Basics.TemplateFile import TemplateFile
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

def calcRefinementLevel(globalLength, localLength):
    return int(round(math.log(globalLength / localLength, 2)))
    

def setup():
    work = get_work()
    config = Config()
    snappy = Snappy()
    feature = Feature()

    globalLength = config.getElementLength()
    
    for fan in config.getFans():
        snappy.addFan(fan)
        
    for blank in config.getBlanks():
        snappy.addBlank(blank)
           
    for baffle in config.getBaffles():
        snappy.addBaffle(baffle)
           
    for solid in config.getSolids():
        snappy.addSolid(solid)
        
    for refinementRegion in config.getRefinementRegions():
        snappy.addRefinementRegion(refinementRegion)
        
    for geom in config.getSolids() + config.getFans() + config.getBlanks() + config.getBaffles():
        localLength = config.getElementLength(geom)
        refinementLevel = calcRefinementLevel(globalLength, localLength)
        snappy.setRefinement(refinementLevel, geom)
        feature.addGeom(geom)

    for geom in config.getRefinementRegions():
        localLength = config.getElementLength(geom)
        refinementLevel = calcRefinementLevel(globalLength, localLength)
        snappy.setRegionRefinement(refinementLevel, geom)
        
    
    boundingBox = config.getBoundingBox()
    dist = config.getBoundingBoxDistance()

    fluidBoundaries = ([x - dist for x in boundingBox[0:3]] + 
                       [x + dist for x in boundingBox[3:6]])

    location = [x - .00111 for x in fluidBoundaries[3:6]]
    snappy.setLocation(location)

    bmName = os.path.join(work.polyMeshDir(), "blockMeshDict")

#    template=TemplateFile(bmName + ".template")
#    template.writeToFile(bmName, {'minx': fluidBoundaries[0],
#                                  'miny': fluidBoundaries[1],
#                                  'minz': fluidBoundaries[2],
#                                  'maxx': fluidBoundaries[3],
#                                  'maxy': fluidBoundaries[4],
#                                  'maxz': fluidBoundaries[5],
#                                  'size': globalLength})

    minx = fluidBoundaries[0]
    miny = fluidBoundaries[1]
    minz = fluidBoundaries[2]
    maxx = fluidBoundaries[3]
    maxy = fluidBoundaries[4]
    maxz = fluidBoundaries[5]    

    blockMesh = ParsedParameterFile(bmName)
    blockMesh["vertices"] = [
        "(%.6f %.6f %.6f)" % (minx, miny, minz),
        "(%.6f %.6f %.6f)" % (maxx, miny, minz),
        "(%.6f %.6f %.6f)" % (maxx, maxy, minz),
        "(%.6f %.6f %.6f)" % (minx, maxy, minz),
        "(%.6f %.6f %.6f)" % (minx, miny, maxz),
        "(%.6f %.6f %.6f)" % (maxx, miny, maxz),
        "(%.6f %.6f %.6f)" % (maxx, maxy, maxz),
        "(%.6f %.6f %.6f)" % (minx, maxy, maxz)]
    
    numx = int((maxx-minx)/globalLength)
    numy = int((maxy-miny)/globalLength)
    numz = int((maxz-minz)/globalLength)
    
    blockMesh["blocks"][2] = "(%d %d %d)" % (numx, numy, numz)
    blockMesh.writeFile()


