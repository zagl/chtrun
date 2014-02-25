# -*- coding: utf-8 -*-

import os
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from definitions import *

class Config(object):
    def __init__(self):
        self.configSections = [
            "solids", 
            "blanks", 
            "baffles", 
            "rotations", 
            "refinements", 
            "fluids",
        ]
        
        write = False
    
        self.path = config_file
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                f.write(dictHeader)
                
        self.dict = ParsedParameterFile(self.path)
        name = "global"
        if name not in self.dict:
            globalDict = {
                "elementLength": 0.008,
                "fluidDistance": 0.01,
                "velocity": [0., 0., 0.],
                "gravity": [0., 0., -9.81],
                "tunnel": False,
                "temperature": 293.15,
                "temperatureIn": 293.15,
                "boundingBox": [0.,0.,0.,1.,1.,1.],
            }
            self.dict[name] = globalDict
            write = True
            
        for section in self.configSections:
            if section not in self.dict:
                self.dict[section] = {}
                write = True
        
        if write:
            self.dict.writeFile()
        
    def __getSection(self, name):
        for section in self.configSections:
            if name in self.dict[section]:
                return section
    
    def getSolids(self):
        return self.dict["solids"].keys()
        
    def getBlanks(self):
        return self.dict["blanks"].keys()
        
    def getBaffles(self):
        return self.dict["baffles"].keys()
        
    def getFluids(self):
        return self.dict["fluids"].keys()
        
    def getFans(self):
        return self.dict["rotations"].keys()
        
    def getRefinementRegions(self):
        return self.dict["refinements"].keys()
    
    def getElementLength(self, name="global"):
        if name == "global":
            return self.dict[name]["elementLength"]
        else:
            section = self.__getSection(name)
            return self.dict[section][name]["elementLength"]
    
    def setElementLength(self, value, name="global"):
        if naame == "global":
            self.dict[name]["elementLength"] = value
        else:
            section = self.__getSection(name)
            self.dict[section][name]["elementLength"] = value
        self.dict.writeFile()
    
    def getBoundingBox(self):
        return self.dict["global"]["boundingBox"]
        
    def setBoundingBox(self, box):
        self.dict["global"]["boundingBox"] = box
        self.dict.writeFile()
    
    def getBoundingBoxDistance(self):
        return self.dict["global"]["fluidDistance"]
        
    def getVelocity(self):
        return self.dict["global"]["velocity"]
    
    def getGravity(self):
        return self.dict["global"]["gravity"]
        
    def getIsTunnel(self):
        return self.dict["global"]["tunnel"]
        
    def getTemperature(self):
        return self.dict["global"]["temperature"]
        
    def getTemperatureIn(self):
        return self.dict["global"]["temperatureIn"]
    
    def getEmissivity(self, name):
        return self.dict["solids"][name]["emissivity"]
    
    def getConductivity(self, name):
        return self.dict["solids"][name]["conductivity"]
        
    def getPower(self, name):
        return self.dict["solids"][name]["power"]
    
    def getThickness(self, name):
        return self.dict["baffles"][name]["thickness"]
        
    def getAxis(self, name):
        return self.dict["rotations"][name]["axis"]
    
    def getRPM(self, name):
        return self.dict["rotations"][name]["rpm"]
    
    def getRadius(self, name):
        return self.dict["rotations"][name]["radius"]
        
    def setFansInFluid(self, fans, fluid):
        self.dict["fluids"][fluid]["rotations"] = fans
        self.dict.writeFile()
        
    def getFansInFluid(self, fluid):
        return self.dict["fluids"][fluid]["rotations"]
        
    def setBafflesInFluid(self, baffles, fluid):
        self.dict["fluids"][fluid]["baffles"] = baffles
        self.dict.writeFile()
        
    def getBafflesInFluid(self, fluid):
        return self.dict["fluids"][fluid]["baffles"]
        
    def addRefinementRegion(self, name):
        if name not in self.getRefinementRegions():
            refinementDict = { 
                "elementLength": 0.001,
            }
            self.dict["refinements"][name] = refinementDict
            self.dict.writeFile()
        
    def addBlank(self, name):
        if name not in self.getBlanks():
            blankDict = { 
                "elementLength": 0.001,
            }
            self.dict["blanks"][name] = blankDict
            self.dict.writeFile()
        
    def addBaffle(self, name):
        if name not in self.getBaffles():
            baffleDict = {
                "elementLength": 0.001,
                "conductivity": 210.0,
                "thickness": 0.001,
                "emissivity": 0.9,
            }
            self.dict["baffles"][name] = baffleDict
            self.dict.writeFile()
    
    def addSolid(self, name):
        if name not in self.getSolids():
            self.solidDict = {
                "elementLength": 0.001,
                "conductivity": 210.0,
                "emissivity": 0.9,
                "power": 0,
            }
            self.dict["solids"][name] = self.solidDict
            self.dict.writeFile()
    
    def rmSolid(self, name):
        if name in self.getSolids():
            del self.dict["solids"][name]
            self.dict.writeFile()
        
    def addFan(self, name):
        if name not in self.getFans():
            fanDict = {
                "elementLength": 0.001, 
                "axis": [[0,0,0],[0,0,0]],
                "radius": 0.0,
                "rpm": 0.0,
            }
            self.dict["rotations"][name] = fanDict
            self.dict.writeFile()
        
    def rmFan(self, name):
        if name in self.getFans():
            del self.dict["rotations"][name]
            self.dict.writeFile()
            
    def addFluid(self, name):
        if name not in self.getFluids():
            fluidDict = {
                "rotations": [],
                "baffles": [],
            }
            self.dict["fluids"][name] = fluidDict
            self.dict.writeFile()
        
    def rmFluid(self, name):
        if name in self.getFluids():
            del self.dict["fluids"][name]
            self.dict.writeFile()
        
        
        
        

