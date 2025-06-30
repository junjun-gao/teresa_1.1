import os

from slcStack.dorisSlcStack import dorisSlcStack
from slcStack.snapSlcStack import snapSlcStack  

from coregistion.dorisCoregistion import dorisCoregistion
from coregistion.snapCoregistion import snapCoregistion

def createSlcStack(parms_path):
    """
    Create a stack of SLC images from the given parameters.
    
    Parameters:
        parms_path (dict): A dictionary containing the parameters for creating the SLC stack.
    
    Returns:
        None
    """
    
    with open(parms_path,'r') as inp:
        parms = eval(inp.read())
    
    parms_file_name = os.path.basename(parms_path)
    print(parms_file_name)
    if parms_file_name == 'snap.parms':
        return snapSlcStack(parms)
    elif parms_file_name == 'doris.parms':
        return dorisSlcStack(parms)
    else:
        raise ValueError("The specified filename is incorrect. Please verify and try again.")



def createCoregistion(parms_path, slc_stack):
    """
    Create a coregistration object from the given parameters.
    
    Parameters:
        params (dict): A dictionary containing the parameters for creating the coregistration object.
    
    Returns:
        None
    """
    for outer_key, inner_dict in data.items():
        print(f"外层键: {outer_key}")
        for inner_key, value in inner_dict.items():
            print(f"  内层键: {inner_key}, 值: {value}")

    with open(parms_path,'r') as inp:
        parms = eval(inp.read())
    
    parms_file_name = os.path.basename(parms_path)

    if parms_file_name == 'snap.parms':
        return snapCoregistion(parms, slc_stack)
    elif parms_file_name == 'doris.parms':
        return dorisCoregistion(parms, slc_stack)
    else:
        raise ValueError("The specified filename is incorrect. Please verify and try again.")

