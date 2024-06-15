
import FreeCAD

# import numpy as np
from scipy.optimize import fsolve
# https://realpython.com/python-pretty-print/
# import pprint
# import re
import time




## bare FPO w/ driving animator

def create_tinyAnimator(obj_name = 'tinyAnimator'):
    """
    bare FeaturePython with attached solver for reverse kinematic problem
    """

    obj = FreeCAD.ActiveDocument.addObject('App::FeaturePython', obj_name)
    # rkSolve.rkSolver(obj)
    tinyAnimator(obj)

    # App.ActiveDocument.recompute()
    return obj

class tinyAnimator():
    def __init__(self, obj):
        """
        create empty solver object
        all parameters and communication goes via Properties
        """

        self.Type = 'tinyAnimator'
        obj.Proxy = self


        # properties
        grp = 'Config'

        # frequency of updates
        obj.addProperty("App::PropertyTime", "tick", grp,
            'time paused between adjacent animation steps')

        # number of steps
        obj.addProperty("App::PropertyInteger", 'steps', grp,
            'number of steps for a full animation cycle')

        # idle value
        obj.addProperty("App::PropertyFloat", 'idle_val', grp,
            'output value if Animator is not running')

        grp = 'Control'
        # execute control flags
        obj.addProperty("App::PropertyBool", "run_now", grp,
            "set true to run Animator - once run_cont=False; 'armed/disarmed' for 'cont'")
        obj.addProperty("App::PropertyBool", "run_cont", grp,
            "set true for continous animation, masked by disarmed")


        # one single output (0...1)
        obj.addProperty("App::PropertyFloat", "output", "Out",
            "output of the animator; cycles 0...1, bind your expressions hereto")
        obj.setPropertyStatus('output', ['ReadOnly', 'Transient', 'Output', 14, 21])


    def onDocumentRestored(self, obj):
        obj.Proxy = self


    def execute(self, obj):
        """
        Called on document recompute
        """
        print('Recomputing {0:s} ({1:s})'.format(obj.Name, self.Type))

        if not getattr(obj, "run_now", None):

            idle = obj.idle_val
            obj.output= idle

            return None

        print ("#### animating not yet implemented")
