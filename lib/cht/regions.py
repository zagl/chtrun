# -*- coding: utf-8 -*-

import os, shutil, subprocess
from Config import Config
from definitions import *

def regions():
    work = get_work()
    config = Config()

    geomDir = geom_dir
    geoms=[]
    for geom in os.listdir(geomDir):
        if geom.endswith("stl"):
            geom = os.path.basename(geom)
            geom = os.path.splitext(geom)[0]
            geoms.append(geom)
    
    
    x = []
    y = []
    z = []
    for geom in geoms:
        isBlank = False
        stlname = geom + ".stl"
        source = os.path.join(geomDir, stlname)
        target = os.path.join(work.constantDir(), "triSurface", stlname)
        shutil.copy(source, target)
        if "ROT" in geom:
            config.addFan(geom)
        elif "FINE" in geom:
            config.addRefinementRegion(geom)
            isBlank = True
        elif "__" in geom:
            config.addBaffle(geom)
        elif "_" in geom:
            config.addBlank(geom)
            isBlank = True
        else:
            for folder in ["constant", "system"]:
                template = os.path.join(region_template_dir, folder, "SOLID")
                target = os.path.join("run", folder, geom)
                if not os.path.exists(target):
                    shutil.copytree(template, target)
            config.addSolid(geom) 
        
        if not isBlank:
            with open(source, 'r') as f:
                for l in f:
                    if "vertex" in l:
                        v = [float(i) for i in l.split()[1:]]
                        x.append(v[0])
                        y.append(v[1])
                        z.append(v[2])
        
    
    config.setBoundingBox([min(i) for i in x, y, z] + [max(i) for i in x, y, z])
    

    for solid in config.getSolids():
        if solid not in geoms:
            config.rmSolid(solid)

    for fan in config.getFans():
        if fan not in geoms:
            config.rmFan(fan)
    
    

