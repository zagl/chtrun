# -*- coding: utf-8 -*-

import os
from ..definitions import *
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

class Snappy(object):
    def __init__(self):
        self.work = get_work()
        self.path = os.path.join(self.work.systemDir(), "snappyHexMeshDict")
        self.dict = ParsedParameterFile(self.path)
        self.castDict = self.dict["castellatedMeshControls"]
    
    def __addGeometry(self, name):
        self.geometryDict = {
            'type': 'triSurfaceMesh', 
            'name': name,
        }
        self.dict["geometry"][name + ".stl"] = self.geometryDict
        
    def __addFeature(self, name):
        self.featuresDict = {
            "file": '"%s.eMesh"' % name,
            "level": 0,
        }
        if self.featuresDict not in self.castDict["features"]:
            self.castDict["features"].append(self.featuresDict)
            
    def __addEmpty(self, name):
        self.castDict["refinementSurfaces"][name] = {
            "level": [2, 2],
        }
    
    def addSolid(self, name):
        self.__addGeometry(name)
        self.__addFeature(name)
        self.castDict["refinementSurfaces"][name] = {
            "level": [2, 2],
            "faceZone": name,
            "cellZone": name,
            "cellZoneInside": "inside"
        }
        self.dict.writeFile()
        
    def addBaffle(self, name):
        self.__addGeometry(name)
        self.__addFeature(name)
        self.castDict["refinementSurfaces"][name] = {
            "level": [2, 2],
            "faceZone": name,
            "faceType": "internal",
        }
        self.dict.writeFile()
        
    def addBlank(self, name):
        self.__addGeometry(name)
        self.__addFeature(name)
        self.__addEmpty(name)
        self.dict.writeFile()
        
    def addFan(self, name):
        self.__addGeometry(name)
        self.__addFeature(name)
        self.__addEmpty(name)
        self.dict.writeFile()
         
    def addRefinementRegion(self, name):
        self.__addGeometry(name)
        self.castDict["refinementRegions"][name] = {
            "mode": "inside",
            "levels": [1.0, 4],
        }
        self.dict.writeFile()
        
    def rmGeom(self, name):
        self.dict["geometry"].pop(name + ".stl", None)
        self.castDict["refinementSurfaces"].pop(name, None)
        for feature in self.castDict["features"]:
            if name not in feature["file"]:
                self.castDict["features"].remove(feature)
        self.dict.writeFile()

    def setLocation(self, center):
        self.castDict["locationInMesh"] = "(%.5f %.5f %.5f)" \
                                          % (center[0], center[1], center[2])
        self.dict.writeFile()
        
    def setRefinement(self, refinement, name):
        self.castDict["refinementSurfaces"][name]["level"] = [refinement, 
                                                              refinement]
        self.dict.writeFile()
        
    def setRegionRefinement(self, refinement, name):
        self.castDict["refinementRegions"][name]["levels"] = [[1.0, refinement]]
        self.dict.writeFile()
        

