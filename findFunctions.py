# from dev.myTinyAsm.trianglesolver import solve
# from dev.myTinyAsm.sheetPyMods_base import *

import importlib

def findFuncs(dirs, files, funcs):

    ## to be replaced later
    # from dev.myTinyAsm.trianglesolver import solve
    # from dev.myTinyAsm.sheetPyMods_base import select
    # from dev.myTinyAsm.sheetPyMods_base import select_args
    pass

    sp_bck = sys.path # backup since we are fiddling
    sys.path = []
    sys.path.append('/home/wrosner/.local/share/FreeCAD/Macro')
    # my_trislv=importlib.machinery.PathFinder.find_module('dev.myTinyAsm.trianglesolver', path='/home/wrosner/.local/share/FreeCAD/Macro')

    # my_trislv1=importlib.machinery.PathFinder.find_module('dev.myTinyAsm.trianglesolver', path=['/home/wrosner/.local/share/FreeCAD/Macro'])

    # my_trislv2=importlib.machinery.PathFinder.find_module('dev.myTinyAsm.trianglesolver')

    try:
        import dev.myTinyAsm.sheetPyMods_base
        import dev.myTinyAsm.trianglesolver
    except:
        print ("exception in import")

    sys.path = sp_bck # restore previous sys.path

    # rv = locals()
    rv = {}
    rv['select'] = select
    rv['solve']  = solve

    return rv