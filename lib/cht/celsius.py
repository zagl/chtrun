# -*- coding: utf-8 -*-

import os
from Config import Config
from Options import Options
from definitions import *
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


def celsius():
    config = Config()
    
    regions = config.getSolids() + config.getFluids()
    
    for region in regions:
        myBasicRunner(["foamCalc", "addSubtract", "T", "subtract", 
                       "-value", "273.15", "-region", region, "-latestTime", 
                       "-resultName", "Temperature"], region)
