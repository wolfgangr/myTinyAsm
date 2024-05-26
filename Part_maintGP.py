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

#/home/wrosner/.local/share/FreeCAD/Macro/dev/myTinyAsm/unveilGlobalPlacement.py
# def create_uGP(obj_name = 'GPinspector'):

# import FreeCAD as App
import FreeCAD
# App = FreeCAD
import os
import re
import datetime
# print(App)
import dev.myTinyAsm.unveilGlobalPlacement as ugp
# print(App)

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

        # obj.addProperty("App::PropertyStringList", "maintainedInspectors", "Base",
        #     'List of Global-Placement-Inspectors currently maintained - autogenerated')
        # obj.setEditorMode('maintainedInspectors', ['ReadOnly'])

    def dumps(self):
        return

    def loads(self, _state):
        return

    def attach(self, obj):
        obj.addExtension("App::OriginGroupExtensionPython")
        obj.Origin = FreeCAD.ActiveDocument.addObject("App::Origin", "Origin")
        #

        obj.addProperty("App::PropertyPythonObject", "maintainedInspectors", "Base",
            'List of Global-Placement-Inspectors currently maintained - autogenerated')
        obj.setEditorMode('maintainedInspectors', ['ReadOnly'])

        obj.addProperty("App::PropertyStringList", "maintainedInspectorFNames", "Base",
            'List of Global-Placement-Inspector FullNames currently maintained - autogenerated')
        obj.maintainedInspectors = []
        obj.setEditorMode('maintainedInspectorFNames', ['ReadOnly'])


    def onDocumentRestored(self, obj):
        self.Object = obj

    def execute(self, obj):
        print('in execute of', obj.FullName)
        doc = FreeCAD.ActiveDocument

        current_insp_list = getattr(obj, 'maintainedInspectors')
        print('current_insp_list*FullName before processing', [i.FullName for i in current_insp_list])

        # search for dependent Links down in GPParts DAG
        for obj_dlnk in obj.InListRecursive:
            ## TBD: this does not work for hidden link arrays
            if ((obj_dlnk.TypeId == 'App::Link' and obj_dlnk.ElementCount == 0 ) or
                    (obj_dlnk.TypeId == 'App::LinkElement')):
                print ('doing inspector with ', obj_dlnk.Name)

                # if dependent Link has no inspector ....
                if 'GPinspector' not in [ itm.Proxy.Type
                        for itm in obj_dlnk.InListRecursive
                        if hasattr(itm, 'Proxy') ] :
                    print ('no inspector')
                    # ... attach inspector ...
                    newGPi = ugp.create_uGP(obj_name = 'PtLnkGPi', arg_tgt = obj_dlnk)
                    # ... and maintain current list
                    current_insp_list.append(newGPi)

        # this throws error in ?? cases if not all items are in doc
        # if we need it, we may write a special safe function for that
        # print('current_insp_list*FullName after adding', [i.Name for i in current_insp_list])

        # remove stale isnpectors belonging to deleted Links
        for check_insp in getattr(obj, 'maintainedInspectors'):
            if getattr (check_insp, 'inspectedObject', False) is None:
                # default 'False' handles the case of 'missing this field althogether'
                # as well as 'checkInsp is None'
                # we do'nt delete this since we do not know what it is
                print ('removing stale inspector',  check_insp.Name )
                doc.removeObject(check_insp.Name)

        current_insp_list = [i for i in current_insp_list if i in doc.Objects]
        print('current_insp_list*FullName after purging', [i.Name for i in current_insp_list])

        # safe in Property for gui check and safe/restore
        obj.maintainedInspectors = current_insp_list
        obj.maintainedInspectorFNames = [i.Name for i in current_insp_list]

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
    newobj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",
            "GPpart", GPpart(),
            ViewProviderGPpart(), True)

                             #"Group",
                             #MyGroup(),
                             #ViewProviderMyGroup(),
                             #True)
    return newobj


