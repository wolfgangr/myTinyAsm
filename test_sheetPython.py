# (c) Wolfgang Rosner 2024 - wolfagngr@github.com
# License: LGPL 2+
#


# import

from dev.myTinyAsm.sheetPythonCustomFunc import *

## TBD #### test config for accessible modules
from dev.myTinyAsm.trianglesolver import solve
from dev.myTinyAsm.sheetPyMods_base import *

# add allowd functions
# sPyMod_model.imported_functions['select_args']=select_args
# sPyMod_model.imported_functions['solve']=solve


##
# test generator

##
# create sketch for testing law of cosine stuff
def add_test_sketch_triangle(skname='Sketch'):
    # add a sketch with a triangle
    sketch = document.addObject('Sketcher::SketchObject', skname)
    v1 = App.Vector(0.000000,0.000000,0)
    v2 = App.Vector(-2.002414,0.000000,0)
    v3 = App.Vector(-0.781895,0.980229,0)
    sketch.addGeometry(Part.LineSegment(v1, v2), False)
    sketch.addGeometry(Part.LineSegment(v1, v3), False)
    sketch.addGeometry(Part.LineSegment(v3, v2), False)
    sketch.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1))
    sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-1))
    sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,1))
    sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,1,2))
    sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,0,2))

    sketch.addConstraint(Sketcher.Constraint('Angle',1,1,0,1,0.897480))
    sketch.setDatum(5,App.Units.Quantity('51.426000 deg'))
    sketch.renameConstraint(5, u'_C')

    sketch.addConstraint(Sketcher.Constraint('Distance',0,2.002414))
    sketch.setDatum(6,App.Units.Quantity('2.002000 mm'))
    sketch.renameConstraint(6, u'a')

    sketch.addConstraint(Sketcher.Constraint('Distance',1,1.253878))
    sketch.setDatum(7,App.Units.Quantity('1.254000 mm'))
    sketch.renameConstraint(7, u'b')

    sketch.addConstraint(Sketcher.Constraint('Distance',2,1.565187))
    sketch.toggleDriving(8)
    sketch.renameConstraint(8, u'c')


    sketch.addConstraint(Sketcher.Constraint('Angle',2,1,1,2,1.567153))
    # sketch.setDatum(9,App.Units.Quantity('89.791000 deg'))
    sketch.toggleDriving(9)
    sketch.renameConstraint(9, u'_A')

    sketch.addConstraint(Sketcher.Constraint('Angle',0,2,2,2,0.676887))
    sketch.toggleDriving(10)
    sketch.renameConstraint(10, u'_B')


##
# start setup of test document


# get or create document object with some part in it
document = App.ActiveDocument
if document is None:
    document = App.newDocument('Part Attachment Example')
    document.addObject('App::Part','Part')
    add_test_sketch_triangle()

# create sheet
psh = create_pySheet('pySheetrecalc', document)

# add test property using select_args
testprop = CONST_DEF_prefix + '_test'
psh.addProperty('App::PropertyStringList', testprop, CONST_DEF_prefix ,
            'test data for custom python')
setattr(psh, testprop, ['select_args', '2', '"foo"', "'bar'",
        '=<<tralala>>', '=Part.Label', '=Part.Placement',
        'noclue', '3', '7/8', '=8/9']
    )

# add test property for triangle solver
testprop = CONST_DEF_prefix + '_triangle'
psh.addProperty('App::PropertyStringList', testprop, CONST_DEF_prefix ,
            'test data for custom python')
setattr(psh, testprop, ['solve', '=Sketch.Constraints.a/1mm', '=Sketch.Constraints.b/1mm', '', '', '', '=Sketch.Constraints._C / 180 ° * pi']
    )


# add cell content to display triangle solver results
# ensure creation of cpy_res_triangle Property to avoid error stakkato on startup
psh.recompute()


resref = '=cpy_res_triangle'
psh.set('A1', '=Sketch.Label')  # dummy to set DAG relation to trigger recompute
psh.set('B1', resref)
for i in range(6):
    psh.set(f"A{i+2}", str(i))
    psh.set(f"B{i+2}",  f"{resref}[A{i+2}]")
    if i < 3:
        psh.set(f"C{i+2}",  f"= B{i+2} * 1 mm")
    else:
        psh.set(f"C{i+2}",  f"= B{i+2} * 180° / pi")

# add config values for automagically 'evalidate'ing test custom modules

# setattr(obj, CONST_CFG_prefix + '_dirs', ['', ':Macro', ':Mod', ':FCStd'])
# pfxdir =  CONST_CFG_prefix + '_dirs'
# dirlist = getattr(psh, pfxdir)
# dirlist.append(':Macro/dev/myTinyAsm')
# setattr(psh, pfxdir, dirlist)

# setattr(psh, CONST_CFG_prefix + '_files', ['trianglesolver.py', 'sheetPyMods_base.py'])
setattr(psh, CONST_CFG_prefix + '_prefix',     'dev.myTinyAsm')
setattr(psh, CONST_CFG_prefix + '_modules',   ['trianglesolver', 'sheetPyMods_base'])
setattr(psh, CONST_CFG_prefix + '_functions', ['select_args', 'solve'])

## setup done

document.recompute()