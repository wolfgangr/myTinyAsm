# .local/share/FreeCAD/Macro/dev/myTinyAsm/unveilGlobalPlacement.py
# upon recompute, scan all first level child objects of linked file
# and write their real global placment to a Parameter so it can be read
# from FreeCAD expressions
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

parameter_group_name = "getGP" # no trailing _ !
tooltip = "retrieved Global Placement List of sub-Object - read only"
# ======================================


import FreeCAD as App
import os
import re
import datetime

# filePath = os.getcwd()
# filePath = os.path.dirname(sys.argv[0])
# https://stackoverflow.com/questions/52778687/nameerror-file-is-not-defined
#       (OMG....)
def dummy(): pass
script_path = (dummy.__code__.co_filename)
filePath = os.path.dirname(script_path)     # (__file__)
# iconPath = filePath + "/icons/myIcon.svg"
# iconPath = filePath + "/icons/myIcon.svg"
iconPath = filePath + icon_rel_path
print ('iconPath:', iconPath)

# https://wiki.freecad.org/FeaturePython_Custom_Properties
def sync_GPParams(obj, pgname = parameter_group_name, new_paramList = ['foo','bar'] ):

    # old_param_list = map-filter ( $1, /(pgname)(.*)/
    old_paramList = []
    for prm in obj.PropertiesList:
        match = re.search(f"^{pgname}_(.*)", prm)
        if match:
            old_paramList.append( match.groups()[0] )

    print ('old_paramList:', old_paramList)
    print ('new_paramList:', new_paramList)
    for prm in new_paramList:
        pg_prm = pgname + '_' + prm  #.rstrip('.')
        if not (prm in old_paramList):
            print('create param: ' + pg_prm)
            obj.addProperty("App::PropertyPlacementList", pg_prm, pgname, tooltip)

    for prm in old_paramList:
        pg_prm = pgname + '_' + prm  # .rstrip('.')
        if not (prm in new_paramList):
            print('delete param: ' + pg_prm)
            obj.removeProperty(pg_prm)



def create_uGP(obj_name = 'GPinspector'):
    """
    Object creation method
    """

    obj = App.ActiveDocument.addObject('App::FeaturePython', obj_name)
    GPinspector(obj)
    App.ActiveDocument.recompute()
    return obj

class GPinspector():
    def __init__(self, obj):
        """
        Default constructor
        """
        self.Type = 'GPinspector'
        obj.Proxy = self
        obj.addProperty('App::PropertyString', 'Description', 'Base', 'Box description')
        obj.addProperty("App::PropertyLink", "inspected_Object", "Base", 'The object whose subobjects real global placment values shall be retrieved')

    def execute(self, obj):
        """
        Called on document recompute
        """
        print('Recomputing {0:s} ({1:s})'.format(obj.Name, self.Type))