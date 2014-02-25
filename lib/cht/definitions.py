# -*- coding: utf-8 -*-

import os
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Execution.BasicRunner import BasicRunner

home = os.path.expanduser("~")
install_dir = os.path.join(home, "OpenFOAM", "python")
template_dir = os.path.join(install_dir, "share", "base")
region_template_dir = os.path.join(install_dir, "share", "region")
cwd = os.getcwd()
work_dir = os.path.join(cwd, "run")
config_file = os.path.join(cwd, "configDict")
geom_dir = os.path.join(cwd, "geom")
orig_dir = os.path.join(geom_dir, "orig")

def get_template():
    if os.path.exists(template_dir):
        return SolutionDirectory(template_dir, archive=None, paraviewLink=False)

def get_work():
    if os.path.exists(work_dir):
        return SolutionDirectory(work_dir, archive=None, paraviewLink=False)

def myBasicRunner(command, add=""):
    run = BasicRunner(argv=command + ["-case", work_dir], silent=True, server=False, 
                      logname=command[0] + ( "." + add if add else add ))
    print "Running " + command[0]
    run.start()

dictHeader = """
FoamFile
{
 version 2.0;
 format ascii; 	
 class dictionary; 	
 object configDict; 	
}
"""
