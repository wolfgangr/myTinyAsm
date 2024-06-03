# from dev.myTinyAsm.trianglesolver import solve
# from dev.myTinyAsm.sheetPyMods_base import *

def findFuncs(dirs, files, funcs):

    ## to be replaced later
    # from dev.myTinyAsm.trianglesolver import solve
    # from dev.myTinyAsm.sheetPyMods_base import select
    # from dev.myTinyAsm.sheetPyMods_base import select_args
    import dev.myTinyAsm.sheetPyMods_base
    import dev.myTinyAsm.trianglesolver

    # rv = locals()
    rv = {}
    rv['select'] = select
    rv['solve']  = solve

    return rv