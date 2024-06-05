# import dev.myTinyAsm.findFunctions as findFunctions
# inspired by evalidate, but finally implemented without

import importlib
import re
import sys


class sheetPyCEvalidator:
    """ implement evalidate and associated model for sheetPythonCustom """
    def __init__(self, sheet=None,
            prefix='', modules='', functions='', reimport=''):

        self.sheet = sheet
        self.prefix      = prefix       # getattr(obj, dirs)
        self.modules     = modules      # getattr(obj, files)
        self.functions   = functions    #(obj, functions)
        self.reimport    = reimport     # the property name

        self.ready = False

        self.modlist  = {}
        self.funclist = {}
        self.accsFlist = {}



    # func_evd = evalidate.Expr(funcnam, model=sPyMod_model)
    # func_ptr = func_evd.eval()
    # rv = func_ptr(*params)
    ## TBD - de-evalidate
    def sPeval(self, funcnam, *params) :

        self.make_ready() # ensure that our machinery is up to date

        func_ptr = self.accsFlist[funcnam]
        rv = func_ptr(*params)
        return rv

    def _update_modList(self):
        # FreeCAD.getUserMacroDir(True)
        ml = {}  # => import value as key

        pref = getattr(self.sheet, self.prefix, '')
        if pref:
            if not re.match(r"^([\w_]+)(\.[\w_]+)*$", pref):
                raise ValueError(f"module prefix <{pref}> does not match foo.bar.pattern")
        else:
            pref= ''

        mods = getattr(self.sheet, self.modules, [])
        for m in mods:
            if not re.match(r"^([\w_]+)(\.[\w_]+)*$", m):
                print(f"module name <{m}> does not match foo.bar.pattern - ignored")
            else:
                ml[m]= (pref + '.' + m) if pref else m

        if (not ml) and pref:  # i.e. no valid modules defined
            ml[pref] = pref

        if ml:
            self.modlist = ml


    def _update_funcList(self):

        fl = {}
        for key, value in self.modlist.items():

            # resemble the behaviour of 'import value as key'
            mod = sys.modules.get(key)

            if mod:                     # already imported
                importlib.reload(mod)

            else:                       #  if still unknown
                try:
                    # import value as key
                    # https://stackoverflow.com/questions/10675054/how-to-import-a-module-in-python-with-importlib-import-module#10675081
                    # mod = importlib.import_module('.'+key ,  __name__)
                    # mod = sys.modules.get(key)
                    mod = importlib.import_module(value)
                    globals()[key] = mod
                except:
                    print(f"failed to:  import {value} as {key} ")

            if mod:
                mod.__dict__.keys()
                # filter out 'dunders' to get function candidates
                for fcname, fcval in mod.__dict__.items():
                    # ignore __dunder__
                    if  re.match(r"^__[\w]+__$", fcname):
                        continue

                    if callable(fcval):
                        fl[fcname] = fcval
        if fl:
                self.funclist = fl

    # filter all functions in funclist() by user selection
    def accessibleFunctions(self):
        return  { fname: fref
                    for (fname, fref) in self.funclist.items()
                    if fname in self.sheet.cpy_cfg_functions
                }

    ##
    def touched(self):
        self._set_reimport(False)

    def _set_reimport(self, bl = False):
        setattr(self.sheet, self.reimport, bl)

    def _get_reimport(self):
        return bool( getattr(self.sheet, self.reimport, False))



    def _update(self):
        # if not self.ready:
        self._update_modList()
        self._update_funcList()
        self.accsFlist = self.accessibleFunctions()
        self.ready = True

    def make_ready(self):
        if self.ready:
            return True
        self._update()
        if self.ready:
            return True
        else:
            raise RuntimeError("update failed")













