import FreeCAD


# basic testing dummy
def select(mylist: list, pos: int):
    try:
        return mylist[pos]

    except:
        return None

# wrapper for arg list
def select_args(pos: int, *args):
    return select(args, pos)


# and my big topic: real global Placement of linked elements
def real_global_placement(link: str, subobj:str):
    print (f"retrieving placment of {subobj} in {link}")
    doc = FreeCAD.ActiveDocument
    lnk = doc.getObject(link)
    if not lnk:
        return None

    plc = lnk.getSubObject(subobj.rstrip('.')+'.' , retType=3)
    print(plc)
    return plc

def noop():
    pass

