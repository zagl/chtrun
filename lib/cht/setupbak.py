# -*- coding: utf-8 -*-

import os
from Config import Config
from Options import Options
from definitions import *
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

def setup():
    boundary = {}
    U = {'"[^XYZ]*"': {'type': 'fixedValue', 'value': 'uniform (0 0 0)'}}
    T = {
        '"[^XYZF]*"': {
            'type': 'zeroGradient'
        },
        '"F.*"': {
            'type': 'compressible::turbulentTemperatureRadCoupledMixed',
            'Tnbr': 'T',
            'kappa': 'fluidThermo',
            'QrNbr': 'none',	
            'Qr': 'Qr',
            'kappaName': 'none',
            'value': '$internalField',
        }
    }
    p = {'"[^XYZ]*"': {'type': 'fixedFluxPressure', 'value': '$internalField'}}

    work = get_work()

    config = Config()

    solids = config.getSolids()
    fluids = config.getFluids()
    temperature = config.getTemperature()

    path = os.path.join(work.constantDir(), "regionProperties")
    regionProperties = ParsedParameterFile(path)
    regionProperties["regions"][3] = solids
    regionProperties["regions"][1] = fluids
    regionProperties.writeFile()

    for solid in solids:
        fluidFields = ["rho", "mut", "alphat", "epsilon", "k",
                       "U", "p_rgh", "Qr", "G", "IDefault",
                       "rho.gz", "mut.gz", "alphat.gz", "epsilon.gz", "k.gz",
                       "U.gz", "p_rgh.gz", "Qr.gz", "G.gz", "IDefault.gz"]
        for field in fluidFields:
            path = os.path.join(work.initialDir(), solid, field)
            if os.path.exists(path):
                os.remove(path)

        path = os.path.join(work.constantDir(), solid,
                            "thermophysicalProperties")
        solidThermo = ParsedParameterFile(path)
        solidThermo["mixture"]["transport"]["kappa"] = config.getConductivity(solid)
        solidThermo.writeFile()

        path = os.path.join(work.constantDir(), solid,
                            "radiationProperties")

        rad = ParsedParameterFile(path)
        rad["constantAbsorptionEmissionCoeffs"]["emissivity"][2] = config.getEmissivity(solid)
        rad.writeFile()

        power = config.getPower(solid)
        options = Options(solid)
        options.addLowerTempLimit(temperature)
        
        if power != 0:
            options.addHeatSource(power)
        else:
            options.rmHeatSource()

        path = os.path.join(work.systemDir(), solid, "changeDictionaryDict")
        changeDict = ParsedParameterFile(path)
        changeDict['dictionaryReplacement']['T']['internalField'] = "uniform " + temperature
        changeDict.writeFile()
        myBasicRunner(["changeDictionary", "-region", solid], solid)
      
      

    v = config.getVelocity()
    g = config.getGravity()
    isTunnel = config.getIsTunnel()
    
    isFree = True
    for (direction, value) in zip(['X', 'Y', 'Z'], v):
        if value == 0:
            continue
        elif value < 0:
            vdir = ["max", "min"]
            d = "-%s" % direction
            isFree = False
            break
        elif value > 0:
            vdir = ["min", "max"]
            d = "+%s" % direction
            isFree = False
            break
            
    for (direction, value) in zip(['X', 'Y', 'Z'], g):
        if value == 0:
            continue
        elif value < 0:
            gdir = ["min", "max"]
            g = "-%s" % direction
            break
        elif value > 0:
            gdir = ["max", "min"]
            g = "+%s" % direction
            break
                        

#    v = config.getVelocity()
#    d = config.getDirection()
#    isTunnel = config.getIsTunnel()
#    g = config.getGravity()
#    if g[0] == '-':
#        gdir = ["min", "max"]
#    else:
#        gdir = ["max", "min"]
#        
#    if d[0] == '-':
#        vdir = ["max", "min"]
#    else:
#        vdir = ["min", "max"]
#        
    if isFree:
        U.update( 
            {
                '"%s.|%s[^%s]"' % (gdir[0], gdir[1], g[1]):
                {
                    'type': 'pressureInletOutletVelocity',
                    'value': 'uniform (0 0 0)',
                },
                '"%s%s"' % (gdir[1], g[1]):
                {
                    'type': 'inletOutlet',
                    'inletValue': 'uniform (0 0 0)',
                    'value': 'uniform (0 0 0)',
                }
            }
        )
        T.update( 
            {
                '"(min|max)."':
                {
                    'type': 'inletOutlet',
                    'inletValue': '$internalField',
                    'value': '$internalField',
                }  
            }
        )
        p.update( 
            {
                '"%s.|%s[^%s]"' % (gdir[0], gdir[1], g[1]):
                {
                    'type': 'totalPressure',
                    'p0': '$internalField',
                    'U': 'U',
                    'phi': 'phi',
                    'rho': 'rho',
                    'psi': 'none',
                    'gamma': '1',
                    'value': '$internalField'
                },
                '"%s%s"' % (gdir[1], g[1]):
                {
                    'type': 'buoyantPressure',
                    'value': '$internalField',
                }	
            }
        )
    elif isTunnel:
        boundary
        {
            '"(min|max)[^%s]"' % d[1]:
            {
                'type': 'wall'
            }
        }
        U.update( 
            {
                '"%s%s"' % (vdir[0], d[1]):
                {
                    'type': 'fixedValue',
                    'value': '$internalField'
                },
                '"%s%s"' % (vdir[1], d[1]):
                {
                    'type': 'inletOutlet',
                    'value': '$internalField',
                    'inletValue': 'uniform (0 0 0)',
                },
                '"(min|max)[^%s]"' % d[1]:
                {
                    'type': 'fixedValue',
                    'value': 'uniform (0 0 0)'
                },
            }
        )
        T.update( 
            {
                '"%s[^%s]|%s."' % (vdir[1], d[1], vdir[0]):
                {
                    'type': 'fixedValue',
                    'value': '$internalField'
                },
                '"%s%s"' % (vdir[1], d[1]):
                {
                    'type': 'inletOutlet',
                    'value': '$internalField',
                    'inletValue': '$internalField',
                }
            }
        )
        p.update( 
            {
                '"%s[^%s]|%s."' % (vdir[1], d[1], vdir[0]):
                {
                    'type': 'fixedValue',
                    'value': '$internalField'
                },
                '"%s%s"' % (vdir[1], d[1]):
                {
                    'type': 'fixedValue',
                    'value': '$internalField',
                }	
            }
        )
    else:
        if gdir[0] == vdir[1]:
            a = '"%s[^%s%s]|%s."' % (gdir[1], g[1], d[1], gdir[0])
        else:
            a = '"%s[^%s]|%s[^%s]"' % (gdir[1], g[1], gdir[0], d[1])
        
        U.update( 
            {
                '"%s%s"' % (vdir[0], d[1]):
                {
                    'type': 'fixedValue',
                    'value': '$internalField'
                },
                a:
                {
                    'type': 'pressureInletOutletVelocity',
                    'value': 'uniform (0 0 0)',
                },
                '"%s%s"' % (gdir[1], g[1]):
                {
                    'type': 'inletOutlet',
                    'inletValue': 'uniform (0 0 0)',
                    'value': 'uniform (0 0 0)',
                }
            }
        )
        T.update( 
            {
                '"%s%s"' % (vdir[0], d[1]):
                {
                    'type': 'fixedValue',
                    'value': '$internalField'
                },
                '"%s[^%s]|%s."' % (vdir[0], d[1], vdir[1]):
                {
                    'type': 'inletOutlet',
                    'value': '$internalField',
                    'inletValue': '$internalField',
                }
            }
        )
        p.update( 
            {
                a:
                {
                    'type': 'totalPressure',
                    'p0': '$internalField',
                    'U': 'U',
                    'phi': 'phi',
                    'rho': 'rho',
                    'psi': 'none',
                    'gamma': '1',
                    'value': '$internalField'
                },
                '"%s%s"' % (gdir[1], g[1]):
                {
                    'type': 'fixedValue',
                    'value': '$internalField',
                },
                '"%s%s"' % (vdir[0], d[1]):
                {
                    'type': 'fixedFluxPressure',
                    'value': '$internalField',
                }
            }
        )
        

        

    for fluid in fluids:
        options = Options(fluid)
        for fan in config.getFansInFluid(fluid):
            axis = config.getAxis(fan)
            rpm = config.getRPM(fan)
            options.addMRF(fan, axis, rpm)
            
        path = os.path.join(work.systemDir(), fluid, "changeDictionaryDict")
        changeDict = ParsedParameterFile(path)
        changeDict['dictionaryReplacement']['T']['internalField'] = "uniform %s" % temperature
        uBoundary = "uniform (%s)" % ' '.join([str(x) for x in v])
        changeDict['dictionaryReplacement']['U']['internalField'] = uBoundary
        changeDict['dictionaryReplacement']['boundary'] = boundary
        changeDict['dictionaryReplacement']['U']['boundaryField'] = U
        changeDict['dictionaryReplacement']['T']['boundaryField'] = T
        changeDict['dictionaryReplacement']['p_rgh']['boundaryField'] = p
        changeDict.writeFile()
        
        myBasicRunner(["changeDictionary", "-region", fluid], fluid)

        path = os.path.join(work.constantDir(), fluid, "g")
        gfile = ParsedParameterFile(path)
        gfile["value"] = "(%s)" % ' '.join([str(x) for x in config.getGravity()])
        gfile.writeFile()





