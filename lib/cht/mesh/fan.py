# -*- coding: utf-8 -*-

import os, subprocess
import shutil
from ..Config import Config
from ..definitions import *
import numpy


def extendAxis(axis):
    p1 = numpy.array(axis[0])
    p2 = numpy.array(axis[1])
    
    length = 0.001
    vector = p2 - p1
    norm = vector / numpy.linalg.norm(vector)
    extension = norm * length
    
    p1e = p1 - extension
    p2e = p2 + extension
    
    return [list(p1e), list(p2e)]


def fan():
    work = get_work()
    
    config = Config()        

    for fluid in config.getFluids():
        boundary_path = os.path.join(work.polyMeshDir(fluid), "boundary" )
        with open(boundary_path, "r") as boundary_file:
            boundary = boundary_file.read()
        
        fans = []
        zones = []
        for fan in config.getFans():
            print fan
            if fan in boundary:
                axis = config.getAxis(fan)
                radius = config.getRadius(fan)
                extended = extendAxis(axis)
                point1 = ' '.join([str(x) for x in extended[0]])
                point2 = ' '.join([str(x) for x in extended[1]])
                zones.append("cellSet %s new cylinderToCell (%s) (%s) %s" % 
                             (fan, point1, point2, radius))
                zones.append("cellZoneSet %s new setToCellZone %s" % (fan, fan))
                fans.append(fan)
        
        if fans:
            config.setFansInFluid(fans, fluid)
            
            setSetFile = os.path.join(work_dir, 
                                      "createRotorZones.%s.setSet" % fluid)
            with open(setSetFile, "w") as fobj:
                fobj.write("\n".join(zones))
                
            myBasicRunner(["setSet", "-batch", setSetFile, "-region", fluid], 
                           "createRotorZones.%s" % fluid)
            



        
