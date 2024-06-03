# (c) Wolfgang Rosner 2024 - wolfagngr@github.com
# License: LGPL 2+
#
# boilerplated from
# https://wiki.freecad.org/Create_a_FeaturePython_object_part_I#Complete_code
# https://wiki.freecad.org/Scripted_objects_with_attachment

import FreeCAD as App
# import os
import re
import datetime
import Spreadsheet

# https://docs.python.org/3.8/library/ast.html#ast.literal_eval
# Safely evaluate an expression node or a string containing a Python literal or container display.
from ast import literal_eval

# from dev.myTinyAsm.spEvalidate import * # as spEvalidate
from dev.myTinyAsm.spEvalidate import evalidate, sPyMod_model


# from xml.sax.handler import ContentHandler
# import xml.sax.handler
import xml.sax

CONST_MYBang = "'#!"
CONST_DEF_prefix ="cpy_def"
CONST_RES_prefix ="cpy_res"
CONST_CFG_prefix ="cpy_cfg"

from dev.myTinyAsm.sheetPyMods_base import *
from dev.myTinyAsm.trianglesolver import solve



# for test case
# from dev.myTinyAsm.sheetPyMods_base import *

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

# required if we overload execute()
def recompute_cells(obj):
    u_range = obj.getUsedRange()
    range_str = u_range[0] + ':' + u_range[1]
    if range_str != '@0:@0':       # if sheet is not empty
        obj.recomputeCells(range_str)

# evaluate parameters from def-List
def eval_param(obj, param: str):
    # remove leading / trailing  spaces
    ps = param.strip()

    # is it a string?
    match = re.search(r"^\'(.*)\'$", ps )
    if match:
        # forward all with quote encapsulation
        return ('"' + match.group(1) + '"')

    match = re.search(r"^\"(.*)\"$", ps )
    if match:
        return ('"' + match.group(1) + '"')

    # '=...' try  FreeCAD Expression;  even matches ...
    #   <<strings>>, cell and object references,  numbers and arithmetic expressions
    match = re.search(r"=(.*)", ps )
    if match:
        try:
            evld = obj.evalExpression( match.group(1) )
            # lets figure out how to interface that to python
            # try 'tick' encapsulation ...
            #   spoils Placement, numbers....
            # return "'" + str(evld) + "'"
            return evld
        except:
            return None

    # try python to eval it:
    try:
        # no encapsulation
        # return eval(ps)
        # secure ast.literal_eval
        return literal_eval(ps)


    except:
        return None



def calc_list_eval(obj, p_list: list[str]):
    if not p_list:
        return None

    funcnam = p_list[0].strip()
    params = [ eval_param(obj, p) for p in p_list[1:] ]
    # print (f"calling {funcnam} with: ", str(params))
    # arglist = ', '.join(params)
    # evalstr= f"{funcnam}({arglist})"
    # print (evalstr)
    # retval = eval(evalstr)
    # https://stackoverflow.com/questions/21100203/passing-arguments-to-python-eval

    # rv = eval(funcnam)(*params)
    # myfunc = eval(funcnam)
    # rv = myfunc(*params)

    # use evalidate instead to validate against malicious code
    # see https://github.com/FreeCAD/FreeCAD/issues/14042#issuecomment-2143963786
    # rv = evalidate.Expr(funcnam, model=sPyMod_model).eval()(*params)
    func_evd = evalidate.Expr(funcnam, model=sPyMod_model)
    func_ptr = func_evd.eval()
    rv = func_ptr(*params)

    # print(rv)
    return rv


## perform calculation
def perform_calculation(obj):
    for prop in obj.PropertiesList:
        match = re.search(f'^{CONST_DEF_prefix}_(.*)', prop)
        if match:
            varname = match.group(1)
            # print (f"matched: {prop} -> {varname}")
            deflist = obj.getPropertyByName(prop)
            prop_res = f"{CONST_RES_prefix}_{varname}"
            result = calc_list_eval(obj, deflist)
            # print (f"to update Property Field {prop_res} with {result} of type {type(result)} ")
            try:
                setattr(obj, prop_res, result)

            except:
                print (f"cannot set {prop_res} - maybe still initializing...")

            obj.touch()
##


def update_res_fields(obj):
    # cycle over function definitions properties
    for prop in obj.PropertiesList:
        match = re.search(f'^{CONST_DEF_prefix}_(.*)', prop)
        if match:
            varname = match.group(1)
            # print (f"matched: {prop} -> {varname}")
            deflist = obj.getPropertyByName(prop)
            if deflist.__class__ is not list:
                raise TypeError(f"prop must be of Type 'App::PropertyStringList' ")
            # find or create matching result property
            prop_res = f"{CONST_RES_prefix}_{varname}"
            # print (f"result:     -> {prop_res}")
            if prop_res not in obj.PropertiesList:
                # obj.addProperty('App::PropertyPythonObject', 'cpy_res_dummy')
                obj.addProperty('App::PropertyPythonObject', prop_res, CONST_RES_prefix,
                    f"result property for {prop}")
                obj.setPropertyStatus(prop_res, 'ReadOnly')
                obj.touch()  # does this recurse??

            # anyway - may be our result has changed
            perform_calculation (obj)
            # ## perform calculation
            # result = calc_list_eval(obj, deflist)
            # # print (f"to update Property Field {prop_res} with {result} of type {type(result)} ")
            # setattr(obj, prop_res, result)
            # obj.touch()


    # remove stale result fields
        # cycle over result definitions properties
    for prop in obj.PropertiesList:
        match = re.search(f'^{CONST_RES_prefix}_(.*)', prop)
        if match:
            varname = match.group(1)
            prop_def = f"{CONST_DEF_prefix}_{varname}"
            if not prop_def in obj.PropertiesList:
                # print(f"stale result property: {prop} - no matching def: {prop_def} - going to delete")
                obj.removeProperty(prop)



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

# class sheetSaxRecompAllCells(xml.sax.handler.ContentHandler):
#     def startElement(self, name, attrs):
#         print(f"BEGIN: <{name}>, {attrs.keys()}")
#         if name == 'Cell':
#             addr = attrs.getValue('address')
#             print(f'doing obj.recomputeCells({addr})')
#             obj.recomputeCells(addr)

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

        obj.addProperty('App::PropertyStringList', CONST_DEF_prefix + '_dummy', CONST_DEF_prefix ,
            'template for custom python function definition')

        obj.addProperty('App::PropertyStringList', CONST_CFG_prefix + '_dirs', CONST_CFG_prefix ,
            'file paths to search for, may start with /; .; ~; :Macro; :Mod; :FCStd')

        setattr(obj, CONST_CFG_prefix + '_dirs', ['', ':Macro', ':Mod', ':FCStd'])

        obj.addProperty('App::PropertyStringList', CONST_CFG_prefix + '_files', CONST_CFG_prefix ,
            'module file names containing user supplied functions, usually *.py, may contain sub-path')

        obj.addProperty('App::PropertyStringList', CONST_CFG_prefix + '_functions', CONST_CFG_prefix ,
            'names of user defined functions allowed to be used')


    def execute(self, obj):
        """
        Called on document recompute
        """
        # print('what shall I do to execute?')
        ## sync res fields
        recompute_cells(obj)
        # update_res_fields(obj)
        perform_calculation (obj)
        recompute_cells(obj)


    def onBeforeChange(proxy,obj,prop):
        # print ("before change:", prop)
        # debug_cells(obj, prop)
        # if prop == 'cells':
        #     xml.sax.parseString(obj.cells.Content, sheetSaxHandler())
        pass

    def onChanged(proxy,obj,prop):
        # print ("changed:", prop)
        # debug_cells(obj, prop)
        # if prop == 'cells':
        #     xml.sax.parseString(obj.cells.Content, sheetSaxHandler())
        # CONST_DEF_prefix
        match = re.match(f"^{CONST_DEF_prefix}_(.*)" , prop)
        if match:
            print ("changed:", prop)
            recompute_cells(obj)
            update_res_fields(obj)
            recompute_cells(obj)

        # pass

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

##
# test generator
# moved out
