# basic testing dummy
def select(mylist: list, pos: int):
    try:
        return mylist[pos]

    except:
        return None

# wrapper for arg list
def select_args(pos: int, *args):
    return select(args, pos)