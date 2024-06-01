# (c) Wolfgang Rosner 2024 - wolfagngr@github.com
# License: LGPL 2+
#


# import

from dev.myTinyAsm.sheetPythonCustomFunc import *

from dev.myTinyAsm.trianglesolver import solve
from dev.myTinyAsm.sheetPyMods_base import *


##
# test generator

# import dev.myTinyAsm.sheetPyMods_base


document = App.ActiveDocument
if document is None:
    document = App.newDocument('Part Attachment Example')
    document.addObject('App::Part','Part')

psh = create_pySheet('pySheetrecalc', document)

testprop = CONST_DEF_prefix + '_test'
psh.addProperty('App::PropertyStringList', testprop, CONST_DEF_prefix ,
            'test data for custom python')
setattr(psh, testprop, ['select_args', '2', '"foo"', "'bar'",
        '=<<tralala>>', '=Part.Label', '=Part.Placement',
        'noclue', '3', '7/8', '=8/9']
    )


document.recompute()