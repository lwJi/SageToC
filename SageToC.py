# SageToC.py
# (c) Liwei Ji 05/2022


############
# packages #
############

import STC_global as Sg
import re

print('Welcome to SageToC (a code generator)')


###########
# Classes #
###########

class STC_Tensor:

    def __init__(self, name, absIndex_list, symmetry):
        self.name = name
        self.absIndex = absIndex_list
        self.symmetry = symmetry


#############
# functions #
#############

# set up manifold and so on

# read variable list and construct tensors
def read_varlist(varlist):
    for var in varlist:
        var_info = var.split(', ')
        fullname = var_info[0]
        name = fullname.split('[')[0]
        absIndex = re.search(r'\[.*?\]', fullname).group(0).strip('[]')
        absIndex_list = None
        symmetry = None
        if(len(absIndex) > 0):
            absIndex_list = absIndex.split(',')
        if(len(var_info) > 1):
            symmetry = var_info[1]

        # set STC_tensor
        globals()[name] = STC_Tensor(name, absIndex_list, symmetry)
        print(var_info)

        # add to var list

        # define Sage_tensor
        Sg.STC_set_tensor(absIndex, name, symmetry)
