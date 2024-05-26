# test case for GPPart
# from recorded macro
#
# (c) Wolfgang Rosner 2024 - wolfagngr@github.com
# License: LGPL 2+

import FreeCAD
import Part
import ManipulatorCMD
# import Commands

doc = App.newDocument()

objPart = doc.addObject('App::Part','Part')
objPart.Label = 'Part'
# App.ActiveDocument.recompute()

objBox = doc.addObject("Part::Box","Box")
objBox.Label = "Cube"
objPart.addObject(objBox)
# App.ActiveDocument.recompute()

objCone = doc.addObject("Part::Cone","Cone")
objCone.Label = "Cone"
objPart.addObject(objCone)
objCone.Radius2 = '1 mm'
objCone.Height = '7.777 mm'
objCone.Angle = '237 deg'

# App.ActiveDocument.recompute()



doc.recompute(None,True,True)
