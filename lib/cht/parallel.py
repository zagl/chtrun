# -*- coding: utf-8 -*-

import os
from Config import Config
from Options import Options
from definitions import *

config = Config()
solids = config.getSolids()
fluids = config.getFluids()

def decompose():
    for region in solids + fluids:
        myBasicRunner(["decomposePar", "-region", region], region)

def reconstruct():
    for region in solids + fluids:
        myBasicRunner(["reconstructPar", "-region", region], region)


