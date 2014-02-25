# -*- coding: utf-8 -*-

import os
from ..definitions import *
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

class Feature(object):
    def __init__(self):
        work = get_work()
        self.path = os.path.join(work.systemDir(), "surfaceFeatureExtractDict")
        self.dict = ParsedParameterFile(self.path)
        self.feature =  {
            "extractionMethod" : "extractFromSurface",
            "extractFromSurfaceCoeffs" : {"includedAngle" : "120" },
            "writeObj" : "no"}
        
    def getGeoms(self):
        return self.dict.keys()
        
    def addGeom(self, geom):    
        self.dict[geom + ".stl"] = self.feature
        self.dict.writeFile()
        
    def rmGeom(self, geom):  
        if geom in self.getGeoms():
            del self.dict[geom + ".stl"]
            self.dict.writeFile()        
        
