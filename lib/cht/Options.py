# -*- coding: utf-8 -*-

import os
from definitions import *
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import numpy


class Options(object):
    def __init__(self, region):
        work = get_work()
        self.path = os.path.join(work.systemDir(region), "fvOptions")
        self.dict = ParsedParameterFile(self.path)
        
    def addMRF(self, fan, axis, rpm):
        self.axis = axis
        self.origin = axis[0]
        self.point = axis[1]
        self.vector = list(numpy.array(self.point) - 
                           numpy.array(self.origin))
        self.rpm = rpm
        self.omega = 2 * numpy.pi * float(self.rpm) / 60
        self.mrf = {
            "type": "MRFSource",
            "active": "on",
            "selectionMode": "cellZone",
            "cellZone": fan,
            "MRFSourceCoeffs": {
                "origin": self.origin,
                "axis": self.vector,
                "omega": self.omega
            }
        }
        self.dict[fan] = self.mrf
        self.dict.writeFile()      
        
    def addHeatSource(self, power):
        self.heatSource = {
            "type": "scalarSemiImplicitSource",
            "active": "on",
            "selectionMode": "all",
            "scalarSemiImplicitSourceCoeffs": {
                "volumeMode": "absolute",
                "injectionRateSuSp": {
                   "h": [-power, 0]
                }
            }
        }
        self.dict["heatSource"] = self.heatSource
        self.dict.writeFile()    
        
    def rmHeatSource(self):
        if "heatSource" in self.dict:
            del self.dict["heatSource"]
            self.dict.writeFile()    
        
    def addLowerTempLimit(self, Tmin):
        self.temperatureLimit = {
            "type": "temperatureLimitsConstraint",
            "active": "on",
            "selectionMode": "all",
            "temperatureLimitsConstraintCoeffs": {
                "Tmin": Tmin,
                "Tmax": 500,
            }
        }
        self.dict["temperatureLimit"] = self.temperatureLimit
        self.dict.writeFile()    
        
        
