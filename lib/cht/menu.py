# -*- coding: utf-8 -*-

from new import new
from regions import regions
import mesh
from setup import setup
from celsius import celsius
from run import run
import parallel
import time
import os

def menu():
    if 'FOAM_APP' in os.environ:
        ans = True
        while ans:
            print """
            1 - Create run directory
            2 - Create regions
            3 - Setup mesh
            4 - Create mesh
            5 - Split mesh
            6 - Create MRF
            7 - Setup case
            8 - Decompose
            9 - Reconstruct
            c - Convert to °C
            r - Run
            a - All run
            
            Quit with enter
            """

            ans = raw_input("Option: ")
            if ans == "1":
                print "Create run directory..."
                new()
                
            elif ans == "2":
                print "Create regions..."
                regions()
                
            elif ans == "3":
                print "Setup mesh..."
                mesh.setup()
                
            elif ans == "4":
                print "Create mesh..."
                mesh.create()
                
            elif ans == "5":
                print "Split mesh..."
                mesh.split()
                
            elif ans == "6":
                print "Create MRF..."
                mesh.fan()
                
            elif ans == "7":
                print "Setup case..."
                setup()
                
            elif ans == "8":
                print "Decompose..."
                parallel.decompose()
                
            elif ans == "9":
                print "Reconstruct..."
                parallel.reconstruct()
                
            elif ans == "c":
                print "Convert to °C..."
                celsius()
                
            elif ans == "r":
                print "Run..."
                run()
                
            elif ans == "a":
                print "All run..."
                new()
                regions()
                mesh.setup()
                mesh.create()
                mesh.split()
                mesh.fan()
                setup()
                run()
                
            elif ans != "":
                print "Error"
            
            time.sleep(.5)
    else:
        print "\nNo OpenFOAM environment found...\n"

