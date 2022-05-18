# STC_global.py
# (c) Liwei Ji 05/2022

import re
from sage.calculus.var import var
from misc_functions import range1 as rg1


####################
# global variables #
####################

# dimension
dimens = None

# manifold name
manifd = None

# for simple export
__all__ = ['dimens', 'manifd']


####################
# global functions #
####################

# set tensors
def define_tensor_and_set_components(absIndex_list, var_name, symmetry_list):

    # set n_convariant and n_contravariant
    n_covariant = 0
    n_contravariant = 0
    if(absIndex_list is not None):
        for index in absIndex_list:
            if '-' in index:
                n_covariant += 1
            else:
                n_contravariant += 1
    n_total = n_contravariant+n_covariant
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

    define_tensors(var_name, n_contravariant, n_covariant,
                   sym_tuple, antisym_tuple)

    set_components(var_name, n_total, sym_tuple, antisym_tuple)


# set components
def set_components(var_name, n_total, sym_tuple, antisym_tuple):
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
                globals()[var_name][a] = var("".join([var_name, str(a)]))
        elif(n_total == 2):
            for a in rg1(index_min, index_max):
                for b in rg1(index_min, index_max):
                    globals()[var_name][a, b] = var(
                        "".join([var_name, str(a), str(b)]))
        elif(n_total == 3):
            for c in rg1(index_min, index_max):
                for a in rg1(index_min, index_max):
                    for b in rg1(index_min, index_max):
                        globals()[var_name][c, a, b] = var(
                            "".join([var_name, str(c), str(a), str(b)]))
        elif(n_total == 4):
            for c in rg1(index_min, index_max):
                for d in rg1(index_min, index_max):
                    for a in rg1(index_min, index_max):
                        for b in rg1(index_min, index_max):
                            globals()[var_name][c, d, a, b] = var(
                                "".join([var_name,
                                         str(c), str(d), str(a), str(b)]))
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
                        globals()[var_name][a, b] = var("".join(
                            [var_name, str(a), str(b)]))
            # [ab]
            elif(antisym_tuple is not None):
                for a in rg1(index_min, index_max):
                    for b in rg1(a+1, index_max):
                        globals()[var_name][a, b] = var("".join(
                            [var_name, str(a), str(b)]))
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
                                globals()[var_name][c, a, b] = var("".join(
                                    [var_name, str(c), str(a), str(b)]))
                # (ab)c
                elif(sym_tuple[0] == 0 and sym_tuple[1] == 1):
                    for a in rg1(index_min, index_max):
                        for b in rg1(a, index_max):
                            for c in rg1(index_min, index_max):
                                globals()[var_name][a, b, c] = var("".join(
                                    [var_name, str(a), str(b), str(c)]))
                else:
                    raise Exception("sym of %s undefined yet!!!" %
                                    var_name)
            elif(sym_tuple is None and antisym_tuple is not None):
                # c[ab]
                if(antisym_tuple[0] == 1 and antisym_tuple[1] == 2):
                    for c in rg1(index_min, index_max):
                        for a in rg1(index_min, index_max):
                            for b in rg1(a+1, index_max):
                                globals()[var_name][c, a, b] = var("".join(
                                    [var_name, str(c), str(a), str(b)]))
                # [ab]c
                elif(antisym_tuple[0] == 0 and antisym_tuple[1] == 1):
                    for a in rg1(index_min, index_max):
                        for b in rg1(a+1, index_max):
                            for c in rg1(index_min, index_max):
                                globals()[var_name][a, b, c] = var("".join(
                                    [var_name, str(a), str(b), str(c)]))
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
                                        globals()[var_name][c, d, a, b] = var(
                                            "".join([var_name, str(c), str(d),
                                                     str(a), str(b)]))
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
                                        globals()[var_name][c, d, a, b] = var(
                                            "".join([var_name, str(c), str(d),
                                                     str(a), str(b)]))
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
                                        globals()[var_name][c, d, a, b] = var(
                                            "".join([var_name, str(c), str(d),
                                                     str(a), str(b)]))
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
                                        globals()[var_name][c, d, a, b] = var(
                                            "".join([var_name, str(c), str(d),
                                                     str(a), str(b)]))
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
                                        globals()[var_name][c, d, a, b] = var(
                                            "".join([var_name, str(c), str(d),
                                                     str(a), str(b)]))
                else:
                    raise Exception("mixed symmetry of %s undefined yet!!!" %
                                    var_name)

            else:
                raise Exception("symmetry of four-index %s undefined yet!!!" %
                                var_name)

        # other num of indexes case
        else:
            raise Exception("symmetry of %s undefined yet!!!" % var_name)


# define tensors
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
