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

# get or create document object with some part in it
document = App.ActiveDocument
if document is None:
    document = App.newDocument('Part Attachment Example')
    document.addObject('App::Part','Part')

# create sheet
psh = create_pySheet('pySheetrecalc', document)

# add test property
testprop = CONST_DEF_prefix + '_test'
psh.addProperty('App::PropertyStringList', testprop, CONST_DEF_prefix ,
            'test data for custom python')
setattr(psh, testprop, ['select_args', '2', '"foo"', "'bar'",
        '=<<tralala>>', '=Part.Label', '=Part.Placement',
        'noclue', '3', '7/8', '=8/9']
    )



##
# add a sketch with a triangle
sketch = document.addObject('Sketcher::SketchObject', 'Sketch')
v1 = App.Vector(0.000000,0.000000,0)
v2 = App.Vector(-2.002414,0.000000,0)
v3 = App.Vector(-0.781895,0.980229,0)
sketch.addGeometry(Part.LineSegment(v1, v2), False)
sketch.addGeometry(Part.LineSegment(v2, v3), False)
sketch.addGeometry(Part.LineSegment(v1, v3), False)


##



document.recompute()