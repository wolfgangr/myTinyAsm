import FreeCAD
import re
import os

PATH_DICT={
'Home':     FreeCAD.ConfigGet('UserHomePath') + '/',
'Root':     '/',
'Macro':    FreeCAD.getUserMacroDir(True) + '/',
'Mod':      FreeCAD.ConfigGet('UserAppData') + 'Mod/',
'Config':   FreeCAD.ConfigGet('UserConfigPath'),
'Cwd':      os.getcwd() + '/'
}


def expandPaths(obj, propname):
    pl_in = getattr(obj, propname)
    pd = PATH_DICT # .copy()
    docname = obj.Document.getFileName()
    pd['FCStd'] = (os.path.dirname(docname) +'/') if docname else ''
    print (pd)
    print(pl_in)





def findFuncs(dirs, files, funcs):

    pass

    sp_bck = sys.path # backup since we are fiddling
    sys.path = []
    sys.path.append('/home/wrosner/.local/share/FreeCAD/Macro')

    try:
        import dev.myTinyAsm.sheetPyMods_base
        import dev.myTinyAsm.trianglesolver
    except:
        print ("exception in import")

    sys.path = sp_bck # restore previous sys.path

    rv = {}
    rv['select'] = select
    rv['solve']  = solve

    return rv