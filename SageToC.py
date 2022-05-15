# SageToC.py
# (c) Liwei Ji 05/2022


############
# packages #
############

import STC_global
import re

print('Welcome to SageToC (a code generator)')


###########
# Classes #
###########

class STC_Tensor:

    def __init__(self, name, absIndex, symmetry=None):
        self.name = name
        self.absIndex = absIndex
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
        absIndex = re.search(r'\[.*?\]',
                             fullname).group(0).strip('[]').split(',')
        symmetry = ''
        if(len(var_info) > 1):
            symmetry = var_info[1]
        globals()[name] = STC_Tensor(name, absIndex, symmetry)
        print(var_info)

        # add to var list
        n_covariant = 0
        n_contravariant = 0
        for index in absIndex:
            if '-' in index:
                n_covariant += 1
            else:
                n_contravariant += 1
        print("tensor type: (", n_covariant, ", ", n_contravariant, ")")

        # define tensors
        STC_global.set_tensors(1, 0, name)
