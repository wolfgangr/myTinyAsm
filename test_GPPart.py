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
objBox.Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(-2,0,1),30))
objPart.addObject(objBox)
# App.ActiveDocument.recompute()

objCone = doc.addObject("Part::Cone","Cone")
objCone.Label = "Cone"
objPart.addObject(objCone)
objCone.Radius2 = '1 mm'
objCone.Height = '7.777 mm'
objCone.Angle = '237 deg'
objCone.Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),10))

# App.ActiveDocument.recompute()
objLCS = doc.addObject('PartDesign::CoordinateSystem', 'LCS')
objLCS.MapMode='NormalToEdge'
objLCS.Support = [(objCone, ('Vertex1', 'Edge1'))]
# objLCS.Support = [(objCone, ('Vertex2', 'Edge5'))]

objPart.addObject(objCone)
objPart.addObject(objLCS)

lnk0 = doc.addObject('App::Link','Link0')
lnk0.setLink(objPart)
lnk0.Label='Link0_single'
lnk0.Placement = App.Placement(App.Vector(-15,-5,0),App.Rotation(App.Vector(0,1,0),-30))

lnk1 = doc.addObject('App::Link','Link1')
lnk1.setLink(objPart)
lnk1.Label='Link1_ar2vis'
lnk1.ElementCount = 2
lnk1.Placement = App.Placement(App.Vector(0,0,14),App.Rotation(App.Vector(0,0,1),33))
lnk1.LinkedChildren[1].Placement = App.Placement(App.Vector(12,0,0),App.Rotation(App.Vector(0,1,0),35))

lnk2 = doc.addObject('App::Link','Link2')
lnk2.setLink(objPart)
lnk2.Label='Link2_ar3hid'
lnk2.ElementCount = 3
lnk2.ShowElement = False
lnk2.Placement = App.Placement(App.Vector(2,0,-2),App.Rotation(App.Vector(-1,1,0),18))
# hidden Element LinkArrays have an empty LinkedChildren list
# lnk2.PlacementList[1] = App.Placement(App.Vector(-2,-5,-8),App.Rotation(App.Vector(1,1,1),-117))
# looks like we can't assign single item in Property
pll = lnk2.PlacementList
print ('pll before:', pll)
pll[1] = App.Placement(App.Vector(-2,-5,-8),App.Rotation(App.Vector(1,1,1),-117))
print ('pll  after:', pll)
lnk2.PlacementList = pll


doc.recompute(None,True,True)
Gui.activeDocument().activeView().viewIsometric()
Gui.SendMsgToActiveView("ViewFit")