# (c) Wolfgang Rosner 2024 - wolfagngr@github.com
# License: LGPL 2+
#
# boilerplated from
# https://wiki.freecad.org/Create_a_FeaturePython_object_part_I#Complete_code
# https://wiki.freecad.org/Scripted_objects_with_attachment

import FreeCAD as App
import Spreadsheet


def recompute_cells(obj):
    u_range = obj.getUsedRange()
    range_str = u_range[0] + ':' + u_range[1]
    if range_str != '@0:@0':       # if sheet is not empty
        obj.recomputeCells(range_str)

# https://forum.freecad.org/viewtopic.php?p=182016#p182016
class pySheetViewProvider:
    ''' basic defs '''

    def __init__(self, obj):
        # obj.Proxy = self
        self.Object = obj

    #	def __getstate__(self):
    #		return None

    #	def __setstate__(self, state):
    #		return None

    def onBeforeChange(proxy,obj,prop):
        print ("VP before change:", prop)

    def onChanged(proxy,obj,prop):
        print ("VP changed:", prop)

class pySheet():
    """
    Simple Custom Box Object
    See Also:
        https://wiki.freecadweb.org/FeaturePython_Objects
    """

    def __init__(self, obj):
        """
        Constructor
        Arguments
        ---------
        - obj: an existing document object or an object created with FreeCAD.Document.addObject('Part::FeaturePython', '{name}').
        """

        self.Type = 'pySheet'

        obj.Proxy = self

        pySheetViewProvider(obj.ViewObject)

        # obj.ViewObject.Proxy = 0  # Mandatory unless ViewProvider is coded


    def execute(self, obj):
        """
        Called on document recompute
        """
        print('what shall I do to execute?')
        recompute_cells(obj)
        # xml.sax.parseString(obj.cells.Content, sheetSaxRecompAllCells())
        # obj.execute(self, obj)

    def onBeforeChange(proxy,obj,prop):
        print ("before change:", prop)


    def onChanged(proxy,obj,prop):
        print ("changed:", prop)


def create_pySheet(obj_name='pySheet', document=None):
    """
    Create a pythonized Spreadsheet.
    """
    if not document:
        document = App.ActiveDocument
    obj = document.addObject('Spreadsheet::SheetPython', obj_name)


    pySheet(obj)


document = App.ActiveDocument
if document is None:
    document = App.newDocument('Part Attachment Example')
psh = create_pySheet('pySheetrecalc', document)
document.recompute()