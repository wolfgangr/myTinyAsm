# sanity checking of user provided code
# see https://github.com/yaroslaff/evalidate/
# assume it lives beneath ourselves in Macro/dev
# .../FreeCAD/Macro/dev$ git clone https://github.com/yaroslaff/evalidate.git

# import dev.evalidate.evalidate as evalidate
# import dev.myTinyAsm.findFunctions as findFunctions
import importlib
import re
# from FreeCAD import getUserMacroDir

# anything is forbidden if not explicitly allowed:
# start by generic math formulae and test what is missing
# sPyMod_model = evalidate.mult_eval_model.clone()
# sPyMod_model = evalidate.base_eval_model.clone()
# sPyMod_model.nodes.extend(['Mult', 'Call', 'Attribute'] )

class sheetPyCEvalidator:
    """ implement evalidate and associated model for sheetPythonCustom """
    # sheet = None
    # model = None
    def __init__(self, sheet=None,
            prefix='', modules='', functions='', reimport=''):

        self.sheet = sheet
        # self.model = evalidate.base_eval_model.clone()
        # self.model.nodes.extend(['Mult', 'Call', 'Attribute'] )
        self.prefix      = prefix       # getattr(obj, dirs)
        self.modules     = modules      # getattr(obj, files)
        self.functions   = functions  #(obj, functions)

        self.reimport    = reimport
        self.ready = False

        self.modlist = {}




    # func_evd = evalidate.Expr(funcnam, model=sPyMod_model)
    # func_ptr = func_evd.eval()
    # rv = func_ptr(*params)
    ## TBD - de-evalidate
    def sPeval(self, funcnam, *params) :
        f_evd = evalidate.Expr(funcnam, model = self.model)
        f_ptr = f_evd.eval
        rv = f_ptr(*params)
        return rv

    # def _update_files(self):
    #     # [ strip_extension(f) for f in getattr(obj, 'cpy_cfg_files', [])  ]
    #     self._file_list = [ findFunctions.strip_extension(f)
    #                 for f in getattr(self.sheet, self.files, [])  ]
    #
    # def _update_dirs(self):
    #     self._path_list = [ p.rstrip('/') for p in
    #             findFunctions.expandPaths(self.sheet, self.dirs) ]

    def _update_modlist(self):
        # FreeCAD.getUserMacroDir(True)
        ml = {}  # => import value as key

        pref = getattr(self.sheet, self.prefix, '')
        if pref:
            if not re.match(r"^([\w_]+)(\.[\w_]+)*$", pref):
                raise(ValueError, f"module prefix <{pref}> does not match foo.bar.pattern")
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




    def _update_funcs(self):

        # self.locals_before = locals() # for debugging

        # sp_bck = sys.path
        # sys.path = self._path_list

        for tg in self._file_list:
            # try:
                module = importlib.import_module(tg)
                importlib.reload(module)
            # except:
            #    print(f"failed to import {tg}")

        # sys.path = sp_bck

        # print (locals())
        # self.locals = locals()
        # self.locals_after = locals() # for debugging

        self._func_dict={}
        for func in getattr(self.sheet, self.functions, []) :
            if re.match(r"^[\w.]+$", func):
                # self._func_dict[func] = eval(func)
                # self._func_dict[func] = locals().get(func)
                self._func_dict[func] = globals().get(func)


        self.model.imported_functions = self._func_dict

    ##
    def touched(self):
        self.reimport = True

    def update(self):
        if self.reimport:
            self._update_modlist()
            self._update_funcs()
            self.reimport = False

        # self._update_funcs()












