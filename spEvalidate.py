# sanity checking of user provided code
# see https://github.com/yaroslaff/evalidate/
# assume it lives beneath ourselves in Macro/dev
# .../FreeCAD/Macro/dev$ git clone https://github.com/yaroslaff/evalidate.git

import dev.evalidate.evalidate as evalidate
import dev.myTinyAsm.findFunctions as findFunctions

# anything is forbidden if not explicitly allowed:
# start by generic math formulae and test what is missing
# sPyMod_model = evalidate.mult_eval_model.clone()
sPyMod_model = evalidate.base_eval_model.clone()
sPyMod_model.nodes.extend(['Mult', 'Call', 'Attribute'] )

class sheetPyCEvalidator:
    """ implement evalidate and associated model for sheetPythonCustom """
    # sheet = None
    # model = None
    def __init__(self, sheet=None, dirs='', files='', functions=''):
        self.sheet = sheet
        self.model = evalidate.base_eval_model.clone()
        self.model.nodes.extend(['Mult', 'Call', 'Attribute'] )
        self.dirs      = dirs       # getattr(obj, dirs)
        self.files     = files      # getattr(obj, files)
        self.functions = functions  #(obj, functions)
        # self.arglist=()


    # func_evd = evalidate.Expr(funcnam, model=sPyMod_model)
    # func_ptr = func_evd.eval()
    # rv = func_ptr(*params)
    def sPeval(self, funcnam, *params) :
        f_evd = evalidate.Expr(funcnam, model = self.model)
        f_ptr = f_evd.eval
        rv = f_ptr(*params)
        return rv

    def _update_files(self):
        # [ strip_extension(f) for f in getattr(obj, 'cpy_cfg_files', [])  ]
        self._file_list = [ findFunctions.strip_extension(f)
                    for f in getattr(self.sheet, self.files, [])  ]

    def _update_dirs(self):
        self._path_list = findFunctions.expandPaths(self.sheet, self.dirs)

    def update(self):
        self._update_files()
        self._update_dirs()












