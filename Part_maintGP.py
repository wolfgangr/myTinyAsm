# companion to unveilGlobalPlacement.py
# keeps GP-inspectors attached to all link childs
# suppsedly consistent for Expressions / Spreadsheet to retrieve
# (c) Wolfgang Rosner 2024 - wolfagngr@github.com
# License: LGPL 2+
#
# boilerplated from
# https://wiki.freecad.org/Std_Part#Scripting

# ======================================
#   config
icon_rel_path = "/icons/PartLinkGlobalPlacementGetter.svg"

parameter_group_name = "GP" # no trailing _ !
tooltip = "maintain gobal Placement inspectors for all link childs"

# ======================================

import os
import re
import datetime


def dummy(): pass
script_path = (dummy.__code__.co_filename)
filePath = os.path.dirname(script_path)     # (__file__)
iconPath = filePath + icon_rel_path
print ('iconPath:', iconPath)


class GPpart(object):
    def __init__(self, obj=None):
        self.Object = obj
        if obj:
            self.attach(obj)

    def dumps(self):
        return

    def loads(self, _state):
        return

    def attach(self, obj):
        obj.addExtension("App::OriginGroupExtensionPython")
        obj.Origin = FreeCAD.ActiveDocument.addObject("App::Origin", "Origin")

    def onDocumentRestored(self, obj):
        self.Object = obj

    def execute(self, obj):
        print('in execute of', obj.FullName)
        current_insp_list =[]
        for obj_in in obj.InListRecursive:
            if re.search( '^GPinspector', obj_in.Name):
                current_insp_list.append(obj_in)
                print ('appended', obj_in.Name)

        print ("current_insp_list:", current_insp_list)

        for obj_in in obj.InListRecursive:
            if ((obj_in.TypeId == 'App::Link' and obj_in.ElementCount == 0 ) or
                    (obj_in.TypeId == 'App::LinkElement')):
                print ('doing inspector with ', obj_in.FullName)



class ViewProviderGPpart(object):
    def __init__(self, vobj=None):
        if vobj:
            vobj.Proxy = self
            self.attach(vobj)
        else:
            self.ViewObject = None

    def attach(self, vobj):
        vobj.addExtension("Gui::ViewProviderOriginGroupExtensionPython")
        self.ViewObject = vobj

    def getIcon(self):
        return iconPath

    def dumps(self):
        return None

    def loads(self, _state):
        return None


def create_GPpart():
    App.ActiveDocument.addObject("Part::FeaturePython",
            "GPpart", GPpart(),
            ViewProviderGPpart(), True)

                             #"Group",
                             #MyGroup(),
                             #ViewProviderMyGroup(),
                             #True)


