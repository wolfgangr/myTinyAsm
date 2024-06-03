import FreeCAD
import re
import os

# pattern for path sanitizing - may be restricted for security policy
# tbd: windows compat
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

    pl_out = []
    for p in  pl_in:
        match = re.match(r"^:([^/]*)((/([^/]+))*)/?$", p)
        if match:
            po = pd.get(match.group(1))
            if match.group(2):
                po = po.rstrip('/')
                po += (match.group(2))
                po += '/'

            pl_out.append(po)

    print  (pl_out)
    return pl_out






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