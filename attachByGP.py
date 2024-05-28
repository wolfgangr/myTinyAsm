
# (c) Wolfgang Rosner 2024 - wolfagngr@github.com
# License: LGPL 2+
#
# boilerplated from
# https://wiki.freecad.org/Create_a_FeaturePython_object_part_I#Complete_code

# ======================================
#   config
icon_rel_path = "/icons/PartLinkGlobalPlacementGetter.svg"
# parameter_group_name = "Inspect_global_placement"
# parameter_group_name = "GPget" # no trailing _ !

parameter_group_name = "GP" # no trailing _ !
tooltip = "retrieved Global Placement of sub-Object - read only"
# ======================================


import FreeCAD as App
import os
import re
import datetime


def create_GPatt(obj_name = 'GPattach', attParent = None, attChild = None ):
    """
    Object creation method
    target priority:
    - "arg_tgt" call argument
    - first obj in GUI selection
    - default: None - to be assigned later
    """

    obj = App.ActiveDocument.addObject('App::FeaturePython', obj_name)
    GPattach(obj)

    if not (attParent and attChild):
        try:
            selection = FreeCADGui.Selection.getSelection()
        except:
            print('no object selected')

    if attParent:
        obj.a1AttParent = attParent
    elif selection:
        obj.a1AttParent = selection.pop(0)

    if attChild:
        obj.b1AttChild = attChild
    elif selection:
        obj.b1AttChild = selection.pop(0)



    App.ActiveDocument.recompute()
    return obj


class GPattach():
    def __init__(self, obj):
        """
        Default constructor
        """
        self.Type = 'GPattach'
        obj.Proxy = self
        # obj.addProperty('App::PropertyString', 'Description', 'Base', 'Box description')

        # Parent
        obj.addProperty("App::PropertyLink", "a1AttParent", "Attachment",
            'The container Object where the attachment anchor resides in ')

        obj.addProperty("App::PropertyEnumeration", "a2AttParentSubobjects", "Attachment",
            'available subObjects of Parents - select Anchor')

        obj.addProperty("App::PropertyPlacement", "a3AttParentSubobjPlacement", "Attachment",
            'global Placement of selected Parent SubObject - autogenerated - changes will be overwritten')

        obj.addProperty("App::PropertyPlacement", "c1AttachmentOffset", "Attachment",
            'offset to be added to parents anchor for effective Anchor Point - editable')

        # Child
        obj.addProperty("App::PropertyLink", "b1AttChild", "Attachment",
            'The container Object where the attachment child pivot resides in ')

        obj.addProperty("App::PropertyEnumeration", "b2AttChildSubobjects", "Attachment",
            'available subObjects of child - select pivot')

        obj.addProperty("App::PropertyPlacement", "b3AttChildSubobjPlacement", "Attachment",
            'global Placement of selected Child SubObject - autogenerated - changes will be overwritten')

        # calculation
        obj.addProperty("App::PropertyPlacement", "c1AttChildPlcInverse", "Attachment",
            'inverse of global Placement of selected Child SubObject - autogenerated - changes will be overwritten')

        obj.addProperty("App::PropertyPlacement", "c2AttChildResultPlc", "Attachment",
            'effective Placement matrix applied to the child = invert(ChildPLC) * AttOffs * ParentPLC')

        # result


        # obj.setEditorMode('inspectedSubobjectList', ['ReadOnly'])

    # def onChanged(self, obj, prop):
    #     # self.execute(obj) # triggers endless recalc loop
    #     try:
    #         # prints "<App> Document.cpp(2705): Recursive calling of recompute"
    #         # but result looks fine
    #         App.ActiveDocument.recompute()
    #     except:
    #         print('App.ActiveDocument.recompute() failed')

    # def onDocumentRestored(self, obj):
        # self.execute(obj)
        # pass

    def execute(self, obj):
        pass
