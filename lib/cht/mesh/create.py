# -*- coding: utf-8 -*-

from ..definitions import *

def create():
    myBasicRunner(["surfaceFeatureExtract"])
    myBasicRunner(["blockMesh"])
    myBasicRunner(["snappyHexMesh", "-overwrite"])
    myBasicRunner(["paraFoam", "-touchAll"])
