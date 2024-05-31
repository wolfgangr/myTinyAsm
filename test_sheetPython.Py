# (c) Wolfgang Rosner 2024 - wolfagngr@github.com
# License: LGPL 2+
#
# boilerplated from
# https://wiki.freecad.org/Create_a_FeaturePython_object_part_I#Complete_code
# https://wiki.freecad.org/Scripted_objects_with_attachment

import FreeCAD as App
import os
import re
import datetime
import Spreadsheet

# from xml.sax.handler import ContentHandler
# import xml.sax.handler
import xml.sax

CONST_MYBang = "'#!"

# check if propObj is 'cells' and if so, dump XML
# otherwise return False
#
def debug_cells(obj, prop):

    if prop != 'cells':
        return False

    propObj = getattr(obj, 'cells')
    #
    # if not hasattr(propObj, 'TypeId'):
    #     return False
    #
    # if not (str(propObj.TypeId) == 'Spreadsheet::PropertySheet'):
    #     return False
    print (propObj.Content)
    return True # propObj.Content

class sheetSaxHandler(xml.sax.handler.ContentHandler):

    def startElement(self, name, attrs):
        print(f"BEGIN: <{name}>, {attrs.keys()}")
        if attrs.__contains__('address') and attrs.__contains__('content'):
            attr = attrs.getValue('address')
            val  = attrs.getValue('content')
            print(f"\t{attr} -> {val}")
            match = re.search(f"^{CONST_MYBang}(.*)", val)
            if match:
                evld = match.groups()[0]
                print(f"\t\tTBD: eval({evld})")

    def endElement(self, name):
        print(f"END: </{name}>")

    def characters(self, content):
        if content.strip() != "":
            print("CONTENT:", repr(content))

class sheetSaxRecompAllCells(xml.sax.handler.ContentHandler):
    def startElement(self, name, attrs):
        print(f"BEGIN: <{name}>, {attrs.keys()}")
        if name == 'Cell':
            obj.recomputeCells(attrs.getValue('address'))

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

        # obj.addProperty('App::PropertyLength', 'Length',
        #                 'Dimensions', 'Box length').Length = 10.0

        # Needed to make this object "attachable",
        # or able to attach parameterically to other objects
        # obj.addExtension('Part::AttachExtensionPython')

    def execute(self, obj):
        """
        Called on document recompute
        """
        print('what shall I do to execute?')
        xml.sax.parseString(obj.cells.Content, sheetSaxRecompAllCells())

    def onBeforeChange(proxy,obj,prop):
        print ("before change:", prop)
        debug_cells(obj, prop)
        if prop == 'cells':
            xml.sax.parseString(obj.cells.Content, sheetSaxHandler())

    def onChanged(proxy,obj,prop):
        print ("changed:", prop)
        debug_cells(obj, prop)
        if prop == 'cells':
            xml.sax.parseString(obj.cells.Content, sheetSaxHandler())


def create_pySheet(obj_name='pySheet', document=None):
    """
    Create a pythonized Spreadsheet.
    """
    if not document:
        document = App.ActiveDocument
    # obj = document.addObject('Part::FeaturePython', obj_name)
    # Spreadsheet::SheetPython
    obj = document.addObject('Spreadsheet::SheetPython', obj_name)


    pySheet(obj)
    # obj.ViewObject.Proxy = 0  # Mandatory unless ViewProvider is coded

    # return obj


document = App.ActiveDocument
if document is None:
    document = App.newDocument('Part Attachment Example')
psh = create_pySheet('pySheetrecalc', document)
document.recompute()