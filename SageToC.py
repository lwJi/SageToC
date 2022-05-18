# STC_global.py
# (c) Liwei Ji 05/2022

import re
from sage.calculus.var import var
from misc_functions import range1 as rg1

print('Welcome to SageToC (a code generator)')

####################
# global variables #
####################

# dimension
dimens = None

# manifold name
manifd = None

# map
map_component_to_varlist = []

# for simple export
__all__ = []


###########################
# SageToC varlist classes #
###########################

class Varlist:

    def __init__(self, varlist):
        self.varlist = varlist
        for var_info in self.varlist:
            # get var infos
            [var_name, n_contravariant, n_covariant,
             sym_tuple, antisym_tuple] = get_var_infos(var_info)
            # define Sage tensor
            define_tensors(var_name, n_contravariant, n_covariant,
                           sym_tuple, antisym_tuple)
            print("defining ", var_name, "...")

    def set_components(self):
        for var_info in self.varlist:
            [var_name, n_contravariant, n_covariant,
             sym_tuple, antisym_tuple] = get_var_infos(var_info)
            n_total = n_contravariant + n_covariant
            manipulate_components("set component", var_name, n_total,
                                  sym_tuple, antisym_tuple)
            print("setting components of ", var_name, "...")


####################
# global functions #
####################

# get var_name, n_contravariant, n_covariant, sym_tuple, anitsym_tuple
# notice the sym_tuple and antisym_tuple can be lists
def get_var_infos(var):
    var_info = var.split(', ')
    # get var_name
    var_name = var_info[0].split('[')[0]
    # get absIndex_list
    absIndex = re.search(r'\[.*?\]', var_info[0]).group(0).strip('[]')
    absIndex_list = None
    if(len(absIndex) > 0):
        absIndex_list = absIndex.split(',')
    # get symmetry_list
    if(len(var_info) == 1):
        symmetry_list = None
    elif(len(var_info) == 2):
        symmetry_list = [var_info[1]]
    elif(len(var_info) == 3):
        symmetry_list = [var_info[1], var_info[2]]
    else:
        raise Exception("symmetry_list of %s undefined yet!!!" % var)

    # set n_convariant and n_contravariant
    n_contravariant = 0
    n_covariant = 0
    if(absIndex_list is not None):
        for index in absIndex_list:
            if '-' in index:
                n_covariant += 1
            else:
                n_contravariant += 1
    # n_total = n_contravariant+n_covariant
    # print("n = ", n_contravariant, " + ", n_covariant, " = ", n_total)
    # set sym_tuple and antisym_tuple
    sym_tuple = None
    antisym_tuple = None
    if(symmetry_list is not None):
        if(len(symmetry_list) < 3):
            # go over different types of symmetries
            for symmetry in symmetry_list:
                symmetry_type = symmetry.split('[')[0]
                # go over different groups of same type of symmetry
                for sublist in re.findall(r'\{.*?\}', symmetry):
                    symmetry_indexlist = sublist.strip('{}').split(',')
                    if(symmetry_type == 'sym'):
                        if(sym_tuple is not None):
                            sym_tuple = [sym_tuple, tuple(
                                [int(i) for i in symmetry_indexlist])]
                        else:
                            sym_tuple = tuple(
                                [int(i) for i in symmetry_indexlist])
                    if(symmetry_type == 'antisym'):
                        if(antisym_tuple is not None):
                            antisym_tuple = [antisym_tuple, tuple(
                                [int(i) for i in symmetry_indexlist])]
                        else:
                            antisym_tuple = tuple(
                                [int(i) for i in symmetry_indexlist])
        else:
            raise Exception("symmetry type of %s undefined yet!!!" % var_name)
        # print("sym_tuple = ", sym_tuple, " antisym_tuple = ", antisym_tuple)

    return [var_name, n_contravariant, n_covariant, sym_tuple, antisym_tuple]


def set_component_and_add_to_map(var_name, a, b, c, d):
    index_list = [index for index in [a, b, c, d] if index is not None]
    index_tuple = tuple(index_list)
    fullname = [n for nlist in [[var_name], [str(a) for a in index_list]]
                for n in nlist]
    if(a is None):
        # globals()[var_name].add_expr(var(var_name))
        pass
    else:
        globals()[var_name][index_tuple] = var("".join(fullname))


# different modes
def manipulate_component(mode, var_name, a=None, b=None, c=None, d=None):
    if(mode == "set component"):
        set_component_and_add_to_map(var_name, a, b, c, d)


def define_tensors(var_name, n_contravariant, n_covariant,
                   sym_tuple=None, antisym_tuple=None):

    # scalar case
    if(n_contravariant+n_covariant == 0):
        # globals()[var_name] = manifd.scalar_field(name=var_name)
        globals()[var_name] = manifd.scalar_field(var(var_name), name=var_name)
    # tensor case
    else:
        globals()[var_name] = manifd.tensor_field(
            n_contravariant, n_covariant, name=var_name,
            sym=sym_tuple, antisym=antisym_tuple)

    # add to export list
    __all__.append(var_name)


# manipulate components
def manipulate_components(mode, var_name, n_total, sym_tuple, antisym_tuple):
    index_min = 0
    index_max = 3

    # scalar case
    if(n_total == 0):
        # globals()[var_name].add_expr(var(var_name))
        pass

    # tensor case without symmetry
    elif(sym_tuple is None and antisym_tuple is None):
        if(n_total == 1):
            for a in rg1(index_min, index_max):
                manipulate_component(mode, var_name, a)
        elif(n_total == 2):
            for a in rg1(index_min, index_max):
                for b in rg1(index_min, index_max):
                    manipulate_component(mode, var_name, a, b)
        elif(n_total == 3):
            for c in rg1(index_min, index_max):
                for a in rg1(index_min, index_max):
                    for b in rg1(index_min, index_max):
                        manipulate_component(mode, var_name, c, a, b)
        elif(n_total == 4):
            for c in rg1(index_min, index_max):
                for d in rg1(index_min, index_max):
                    for a in rg1(index_min, index_max):
                        for b in rg1(index_min, index_max):
                            manipulate_component(mode, var_name, c, d, a, b)
        else:
            raise Exception("tensor type of %s undefined yet!!!" % var_name)

    # tensor case with symmetry
    else:
        # two indexes case
        if(n_total == 2):
            # (ab)
            if(sym_tuple is not None):
                for a in rg1(index_min, index_max):
                    for b in rg1(a, index_max):
                        manipulate_component(mode, var_name, a, b)
            # [ab]
            elif(antisym_tuple is not None):
                for a in rg1(index_min, index_max):
                    for b in rg1(a+1, index_max):
                        manipulate_component(mode, var_name, a, b)
            else:
                raise Exception("symmetry of two-index %s undefined yet!!!" %
                                var_name)

        # three indexes case
        elif(n_total == 3):
            if(sym_tuple is not None and antisym_tuple is None):
                # c(ab)
                if(sym_tuple[0] == 1 and sym_tuple[1] == 2):
                    for c in rg1(index_min, index_max):
                        for a in rg1(index_min, index_max):
                            for b in rg1(a, index_max):
                                manipulate_component(mode, var_name, c, a, b)
                # (ab)c
                elif(sym_tuple[0] == 0 and sym_tuple[1] == 1):
                    for a in rg1(index_min, index_max):
                        for b in rg1(a, index_max):
                            for c in rg1(index_min, index_max):
                                manipulate_component(mode, var_name, a, b, c)
                else:
                    raise Exception("sym of %s undefined yet!!!" %
                                    var_name)
            elif(sym_tuple is None and antisym_tuple is not None):
                # c[ab]
                if(antisym_tuple[0] == 1 and antisym_tuple[1] == 2):
                    for c in rg1(index_min, index_max):
                        for a in rg1(index_min, index_max):
                            for b in rg1(a+1, index_max):
                                manipulate_component(mode, var_name, c, a, b)
                # [ab]c
                elif(antisym_tuple[0] == 0 and antisym_tuple[1] == 1):
                    for a in rg1(index_min, index_max):
                        for b in rg1(a+1, index_max):
                            for c in rg1(index_min, index_max):
                                manipulate_component(mode, var_name, a, b, c)
                else:
                    raise Exception("antisymm of %s undefined yet!!!" %
                                    var_name)
            else:
                raise Exception("symmetry of three-index %s undefined yet!!!" %
                                var_name)

        # four indexes case
        elif(n_total == 4):
            if(sym_tuple is not None and antisym_tuple is None):
                if(isinstance(sym_tuple, tuple)):
                    # cd(ab)
                    if(sym_tuple[0] == 2 and sym_tuple[1] == 3):
                        for c in rg1(index_min, index_max):
                            for d in rg1(index_min, index_max):
                                for a in rg1(index_min, index_max):
                                    for b in rg1(a, index_max):
                                        manipulate_component(mode, var_name,
                                                             c, d, a, b)
                    else:
                        raise Exception("sym tuple of %s undefined yet!!!" %
                                        var_name)
                elif(isinstance(sym_tuple, list)):
                    # (cd)(ab)
                    if(sym_tuple[0][0] == 0 and sym_tuple[0][1] == 1
                       and
                       sym_tuple[1][0] == 2 and sym_tuple[1][1] == 3):
                        for c in rg1(index_min, index_max):
                            for d in rg1(c, index_max):
                                for a in rg1(index_min, index_max):
                                    for b in rg1(a, index_max):
                                        manipulate_component(mode, var_name,
                                                             c, d, a, b)
                    else:
                        raise Exception("sym list of %s undefined yet!!!" %
                                        var_name)
                else:
                    raise Exception("sym of %s undefined yet!!!" %
                                    var_name)

            elif(sym_tuple is None and antisym_tuple is not None):
                if(isinstance(antisym_tuple, tuple)):
                    # cd[ab]
                    if(antisym_tuple[0] == 2 and antisym_tuple[1] == 3):
                        for c in rg1(index_min, index_max):
                            for d in rg1(index_min, index_max):
                                for a in rg1(index_min, index_max):
                                    for b in rg1(a+1, index_max):
                                        manipulate_component(mode, var_name,
                                                             c, d, a, b)
                    else:
                        raise Exception("antisym tuple of %s undefined yet!!!"
                                        % var_name)
                elif(isinstance(antisym_tuple, list)):
                    # [cd][ab]
                    if(antisym_tuple[0][0] == 0 and antisym_tuple[0][1] == 1
                       and
                       antisym_tuple[1][0] == 2 and antisym_tuple[1][1] == 3):
                        for c in rg1(index_min, index_max):
                            for d in rg1(c+1, index_max):
                                for a in rg1(index_min, index_max):
                                    for b in rg1(a+1, index_max):
                                        manipulate_component(mode, var_name,
                                                             c, d, a, b)
                    else:
                        raise Exception("antisym list of %s undefined yet!!!" %
                                        var_name)
                else:
                    raise Exception("antisym of %s undefined yet!!!"
                                    % var_name)

            elif(sym_tuple is not None and antisym_tuple is not None):
                if(isinstance(sym_tuple, tuple) and
                   isinstance(antisym_tuple, tuple)):
                    # (cd)[ab]
                    if(sym_tuple[0] == 0 and sym_tuple[1] == 1 and
                       antisym_tuple[0] == 2 and antisym_tuple[1] == 3):
                        for c in rg1(index_min, index_max):
                            for d in rg1(c, index_max):
                                for a in rg1(index_min, index_max):
                                    for b in rg1(a+1, index_max):
                                        manipulate_component(mode, var_name,
                                                             c, d, a, b)
                else:
                    raise Exception("mixed symmetry of %s undefined yet!!!" %
                                    var_name)

            else:
                raise Exception("symmetry of four-index %s undefined yet!!!" %
                                var_name)

        # other num of indexes case
        else:
            raise Exception("symmetry of %s undefined yet!!!" % var_name)
