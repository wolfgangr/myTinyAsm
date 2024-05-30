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
        obj.ViewObject.Proxy = 0  # Mandatory unless ViewProvider is coded

        # obj.addProperty('App::PropertyLength', 'Length',
        #                 'Dimensions', 'Box length').Length = 10.0

        # Needed to make this object "attachable",
        # or able to attach parameterically to other objects
        # obj.addExtension('Part::AttachExtensionPython')

    def execute(self, obj):
        """
        Called on document recompute
        """
        pass


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

    return obj


# document = App.ActiveDocument
# if document is None:
#     document = App.newDocument('Part Attachment Example')
#
# box = create_box('CustomBox', document)
# document.recompute()