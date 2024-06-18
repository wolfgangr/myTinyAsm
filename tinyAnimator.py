
import FreeCAD

# import numpy as np
from scipy.optimize import fsolve
# https://realpython.com/python-pretty-print/
# import pprint
# import re
import threading
import time
import asyncio



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

##
# called after timeout
def nextIteration(obj):
    print('nextIteration')

    # cancel on manual stop?
    if not obj.run_now:
        return

    out = obj.output
    out += 1/obj.steps

    if out > 1:
        if obj.run_cont:        # roll over
            obj.output = 0
            print("iteration rollover restart")
            # return

        else:                   # reached end of single run
            obj.run_now=False
            obj.output = obj.idle_val
            print("animation ending after single run")
            # return

    else:                       # normal increment
        obj.output = out        # this will trigger onChanged where we can reload
        print(f"iteration {out}")
        # return

    # print("recalculate and update ")
    # obj.touch()
    # obj.Document.recompute()
    # FreeCADGui.updateGui()



##

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
        obj.tick = 1

        # number of steps
        obj.addProperty("App::PropertyInteger", 'steps', grp,
            'number of steps for a full animation cycle')
        obj.steps = 30

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

        # self.animator = threading.Thread(target = self.runAnimation, args=(obj,))


    def onDocumentRestored(self, obj):
        obj.Proxy = self

    # # can I call a method as thread function, to access instance properties?
    # async def runAnimation(self,obj):
    #     # await asyncio.sleep(0.1)
    #     sleep(0.1)
    #     out = 0
    #     while True:
    #         print (f"animation output {out}")
    #         obj.output = out
    #         # execute?
    #         obj.touch()
    #         obj.Document.recompute()
    #         FreeCADGui.updateGui()
    #         # time.sleep(obj.tick.Value)
    #         await asyncio.sleep(obj.tick.Value)
    #         # cancel on manual stop
    #         if not obj.run_now:
    #             print("animation ending after manual stop")
    #             break
    #
    #         out += 1/obj.steps
    #         if out > 1:
    #             # restart loop for continous running
    #             if obj.run_cont:
    #                 out = 0
    #             # finish animation after single run
    #             else:
    #                 obj.run_now=False
    #                 obj.output = obj.idle_val
    #                 print("animation ending after single run")
    #                 break
    #
    #     print ("runAnimation ending")



    def onChanged(self, obj, prop):
        match prop:
            # case 'idle_val':
            #    print ('idle_val now is:', obj.idle_val)

            case 'steps':
                if not obj.steps:
                    raise RuntimeWarning('steps = 0 will throw div-by-zero on animation')


            case 'run_now':
                # if obj.run_now and not self.animator.is_alive():
                #     # time.sleep(0.1)
                #     # await asyncio.sleep(0.1)
                #     self.animator.run()
                # # stopping is implemented in thread by checking
                if obj.run_now:
                    timer = threading.Timer(obj.tick.Value, nextIteration, args=(obj,))
                    timer.start()
                    print('started timer')

                else:
                    if hasattr(self, 'timer'):
                        # self.timer.cancel()
                        # obj.output = obj.idle_val
                        print('###TBD### canceled timer')
                    else:
                        print('noop stopped timer')



            case 'output':
                # del self.timer
                timer = threading.Timer(obj.tick.Value, nextIteration, args=(obj,))
                timer.start()
                print('re-started timer for next iteration', timer)

                obj.touch()
                obj.Document.recompute()
                FreeCADGui.updateGui()

            case _:
                print (f'debug: Property {prop} changed - no special handling')

        print ('debug: after onChanged match')




    # def execute(self, obj):
    #     """
    #     Called on document recompute
    #     """
    #     print('Recomputing {0:s} ({1:s})'.format(obj.Name, self.Type))
    #
    #     if not getattr(obj, "run_now", None):
    #
    #         idle = obj.idle_val
    #         obj.output= idle
    #
    #         return None
    #
    #     print ("#### animating not yet implemented")
