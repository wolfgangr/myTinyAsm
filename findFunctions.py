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