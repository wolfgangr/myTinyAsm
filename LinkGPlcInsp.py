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

parameter_group_name = "GP" # no trailing _ !
tooltip = "retrieved Global Placement of sub-Object - read only"
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
def sync_GPParams(obj_svtr, obj_svnd, pgname = parameter_group_name):
    # param List is kept as property of surveilling object
    old_PL = obj_svtr.inspectedSubobjectList

    # .. and has to match subobject List of object under surveillance
    new_PL = list(obj_svnd.getSubObjects())
    new_PL.insert(0, '')
    # new_PL.insert(1, '.')
    if hasattr(obj_svnd, 'Origin'):
        new_PL.insert(1, 'Origin.')

    print ('old_PL', old_PL)
    print ('new_PL', new_PL)

    prm2prop = {} # keep a dictionary of subobj name -> proeprty name
    # add missing params
    for prm in new_PL:
        pg_prm = pgname + '_' + prm.rstrip('.')
        prm2prop[prm] = pg_prm
        if not (prm in old_PL):
            print('create param: ' + pg_prm)
            obj_svtr.addProperty("App::PropertyPlacementList", pg_prm, pgname, tooltip)
            obj_svtr.setEditorMode(pg_prm, ['ReadOnly'])

    # remove stale params
    for prm in old_PL:
        pg_prm = pgname + '_' + prm.rstrip('.')
        if not (prm in new_PL):
            print('delete param: ' + pg_prm)
            obj_svtr.removeProperty(pg_prm)

    obj_svtr.inspectedSubobjectList = new_PL
    return prm2prop


def create_uGPL(obj_name = 'GPLinkInspector', arg_tgt = None):
    """
    Object creation method
    target priority:
    - "arg_tgt" call argument
    - first obj in GUI selection
    - default: None - to be assigned later
    """

    obj = App.ActiveDocument.addObject('App::FeaturePython', obj_name)
    GPLinkInspector(obj)

    if arg_tgt:
        obj.inspectedObject = arg_tgt
    else:
        try:
            target = FreeCADGui.Selection.getSelection()[0]
            obj.inspectedObject = target
            print(f"attached to surveillance of object: <{target.Name}>")
        except:
            print('no valid object selected, leave empty')
            pass

    App.ActiveDocument.recompute()
    return obj

class GPLinkInspector():
    def __init__(self, obj):
        """
        Default constructor
        """
        self.Type = 'GPLinkInspector'
        obj.Proxy = self
        # obj.addProperty('App::PropertyString', 'Description', 'Base', 'Box description')
        obj.addProperty("App::PropertyLink", "inspectedObject", "Base",
            'The object whose subobjects real global placment values shall be retrieved')
        obj.addProperty("App::PropertyStringList", "inspectedSubobjectList", "Base",
            'List of subObjects under surveillance - autogenerated')
        obj.setEditorMode('inspectedSubobjectList', ['ReadOnly'])

    def onChanged(self, obj, prop):
        # self.execute(obj) # triggers endless recalc loop
        try:
            # prints "<App> Document.cpp(2705): Recursive calling of recompute"
            # but result looks fine
            App.ActiveDocument.recompute()
        except:
            print('App.ActiveDocument.recompute() failed')

    # def onDocumentRestored(self, obj):
        # self.execute(obj)
        # pass

    def execute(self, obj):
        """
        Called on document recompute
        """
        print('Recomputing {0:s} ({1:s})'.format(obj.Name, self.Type))
        #
        surveilland = obj.inspectedObject
        if not surveilland:
            print('no object for inspection selected')
            obj.Label=obj.Name
        else:
            ## start inserted link type check
            if surveilland.ElementCount == 0 :
                print('  -- singleton Link: ',  surveilland.Name, ' --')
                # idx_fmt = '{}.'
                eff_elems = 1
                idx_elems = ['']
            # elif len(surveilland.ElementList) == 0 :
            #     print('  -- hidden elem Link Array: ',  surveilland.Name, ' --')
            #     # explore_call(self, obj, linkObj, index, linkElement)
            #     # print ('### TBD ###')
            #     # idx_fmt = '{}.'
            #     eff_elems = surveilland.ElementCount
            #     prefixes = [f"{i}." for i in range(eff_elems)]
            else:
                print('  -- Link Array: ',  surveilland.Name, ' --')
                # prefix= str(index) + '.'
                # idx_fmt = '{}.'
                eff_elems = surveilland.ElementCount
                idx_elems = [f"{i}." for i in range(eff_elems)]
                ## end inserted link type check
            #
            obj.Label='GPinsp_' + surveilland.Label
            paramDict = sync_GPParams(obj, surveilland)
            print ('paramDict:', paramDict)
            # prefix='' # valid for singleton links
            for so in paramDict.keys():
                ## this is now App::PropertyPlacementList
                pg_prm = paramDict[so]
                plcList =[]
                for lelem in idx_elems:

                    # path = prefix + so  #  so.rstrip('.')
                    path = lelem + so
                    plc = surveilland.getSubObject(path, retType = 3)
                    # prop = getattr(obj, pg_prm)
                    # print("checker: so, pg_prm , path, plc:",so, pg_prm , path, plc)
                    plcList.append(plc)

                print ("checker: so, idx_elems, plcList:", so, idx_elems, "\n", plcList)
                setattr(obj, pg_prm, plcList)


