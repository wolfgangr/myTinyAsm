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


import os
import re
import datetime

import dev.myTinyAsm.unveilGlobalPlacement as ugp

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

        obj.addProperty("App::PropertyStringList", "maintainedInspectors", "Base",
            'List of Global-Placement-Inspectors currently maintained - autogenerated')
        obj.setEditorMode('maintainedInspectors', ['ReadOnly'])

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

        # iterate down the DAG for dependent Links
        for obj_dlnk in obj.InListRecursive:
            if ((obj_dlnk.TypeId == 'App::Link' and obj_dlnk.ElementCount == 0 ) or
                    (obj_dlnk.TypeId == 'App::LinkElement')):
                print ('doing inspector with ', obj_dlnk.FullName)

                # if dependent Link has no inspector ....
                if 'GPinspector' not in [ itm.Proxy.Type
                        for itm in obj_dlnk.InListRecursive
                        if hasattr(itm, 'Proxy') ] :
                    print ('no inspector')
                    # ... attach inspector ...
                    # ugp.create_uGP(obj_name = 'GPinspector', arg_tgt = None):
                    newGPi = ugp.create_uGP(obj_name = 'PtLnkGPi', arg_tgt = obj_dlnk)
                    # ... and maintain current list
                    current_insp_list.append(newGPi)

        # # stale
        # for  old inspector list
        old_inspNames_list = getattr(obj, 'maintainedInspectors')
        new_inspNames_list = [i.Name for i in current_insp_list]
        for old_insp in old_inspNames_list:
            # 	if not in in current_inspector_list
            if old_insp not in new_inspNames_list:
                print ('stale inspector:', old_insp, '- check for deletion')
                try:
                    oldIobj = App.getDocument(old_insp)
                    print
                except:
                    print ('cannot find object', old_insp , 'any more')
                    oldIobj = None

                print ('oldIobj:', oldIobj)
                # 	if not found attached part
                if getattr (oldIobj, 'inspectedObject', False) is None:
                    # default 'False' handles the case of missing this field althogether
                    # or oldIobj is None
                    # we do'nt delete this since we do not know what it is
                    print ('removing stale inspector',  old_insp )
                    App.ActiveDocument.removeObject(old_insp)

        # current_inspector_list -> write to old_inspector_list
        obj.maintainedInspectors = current_inspector_list

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


