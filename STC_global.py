# STC_global.py
# (c) Liwei Ji 05/2022

import re
from sage.calculus.var import var

####################
# global variables #
####################
__all__ = ['dimens', 'manifd']

# dimension
dimens = None

# manifold name
manifd = None


def range1(start, end):
    return range(start, end+1)


# set component
def STC_set_component(var_name, a=None, b=None, c=None, d=None):
    # vector case
    if(b is None):
        comp_name = "".join([var_name, str(a)])
        var(comp_name)
        globals()[var_name][a, b, c, d] = var(comp_name)

    # two indexes case


# set tensors
def set_tensor(absIndex_list, var_name, symmetry_list):
    index_min = 0
    index_max = 3
    n_covariant = 0
    n_contravariant = 0

    # set n_convariant and n_contravariant
    if(absIndex_list is not None):
        for index in absIndex_list:
            if '-' in index:
                n_covariant += 1
            else:
                n_contravariant += 1
    n_total = n_contravariant+n_covariant

    # ===========
    # scalar case
    # ===========
    if(n_total == 0):
        globals()[var_name] = manifd.scalar_field(var(var_name), name=var_name)

    # =========================
    # tensor case with symmetry
    # =========================
    elif(symmetry_list is not None):
        # set sym_typle and antisym_tuple
        sym_tuple = None
        antisym_tuple = None
        if(len(symmetry_list) <= 2):
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

        # define tensor
        globals()[var_name] = manifd.tensor_field(
            n_contravariant, n_covariant, name=var_name,
            sym=sym_tuple, antisym=antisym_tuple)

        # set components
        # ----------------
        # two indexes case
        # ----------------
        if(n_total == 2):
            # (ab)
            if(sym_tuple is not None):
                for a in range1(index_min, index_max):
                    for b in range1(a, index_max):
                        globals()[var_name][a, b] = var("".join(
                            [var_name, str(a), str(b)]))
            # [ab]
            elif(antisym_tuple is not None):
                for a in range1(index_min, index_max):
                    for b in range1(a+1, index_max):
                        globals()[var_name][a, b] = var("".join(
                            [var_name, str(a), str(b)]))
            else:
                raise Exception("symmetry of two-index %s undefined yet!!!" %
                                var_name)

        # ------------------
        # three indexes case
        # ------------------
        elif(n_total == 3):
            if(sym_tuple is not None and antisym_tuple is None):
                # c(ab)
                if(sym_tuple[0] == 1 and sym_tuple[1] == 2):
                    for c in range1(index_min, index_max):
                        for a in range1(index_min, index_max):
                            for b in range1(a, index_max):
                                globals()[var_name][c, a, b] = var("".join(
                                    [var_name, str(c), str(a), str(b)]))
                # (ab)c
                elif(sym_tuple[0] == 0 and sym_tuple[1] == 1):
                    for a in range1(index_min, index_max):
                        for b in range1(a, index_max):
                            for c in range1(index_min, index_max):
                                globals()[var_name][a, b, c] = var("".join(
                                    [var_name, str(a), str(b), str(c)]))
                else:
                    raise Exception("sym of %s undefined yet!!!" %
                                    var_name)
            elif(sym_tuple is None and antisym_tuple is not None):
                # c[ab]
                if(antisym_tuple[0] == 1 and antisym_tuple[1] == 2):
                    for c in range1(index_min, index_max):
                        for a in range1(index_min, index_max):
                            for b in range1(a+1, index_max):
                                globals()[var_name][c, a, b] = var("".join(
                                    [var_name, str(c), str(a), str(b)]))
                # [ab]c
                elif(antisym_tuple[0] == 0 and antisym_tuple[1] == 1):
                    for a in range1(index_min, index_max):
                        for b in range1(a+1, index_max):
                            for c in range1(index_min, index_max):
                                globals()[var_name][a, b, c] = var("".join(
                                    [var_name, str(a), str(b), str(c)]))
                else:
                    raise Exception("antisymm of %s undefined yet!!!" %
                                    var_name)
            else:
                raise Exception("symmetry of three-index %s undefined yet!!!" %
                                var_name)

        # -----------------
        # four indexes case
        # -----------------
        elif(n_total == 4):
            if(sym_tuple is not None and antisym_tuple is None):
                if(isinstance(sym_tuple, tuple)):
                    # (ab)cd
                    if(sym_tuple[0] == 0 and sym_tuple[1] == 1):
                        for a in range1(index_min, index_max):
                            for b in range1(a, index_max):
                                for c in range1(index_min, index_max):
                                    for d in range1(index_min, index_max):
                                        globals()[var_name][a, b, c, d] = var(
                                            "".join([var_name, str(a), str(b),
                                                     str(c), str(d)]))
                    # cd(ab)
                    elif(sym_tuple[0] == 2 and sym_tuple[1] == 3):
                        for c in range1(index_min, index_max):
                            for d in range1(index_min, index_max):
                                for a in range1(index_min, index_max):
                                    for b in range1(a, index_max):
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
                        for c in range1(index_min, index_max):
                            for d in range1(c, index_max):
                                for a in range1(index_min, index_max):
                                    for b in range1(a, index_max):
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
                    # [ab]cd
                    if(antisym_tuple[0] == 0 and antisym_tuple[1] == 1):
                        for a in range1(index_min, index_max):
                            for b in range1(a+1, index_max):
                                for c in range1(index_min, index_max):
                                    for d in range1(index_min, index_max):
                                        globals()[var_name][a, b, c, d] = var(
                                            "".join([var_name, str(a), str(b),
                                                     str(c), str(d)]))
                    # cd[ab]
                    elif(antisym_tuple[0] == 2 and antisym_tuple[1] == 3):
                        for c in range1(index_min, index_max):
                            for d in range1(index_min, index_max):
                                for a in range1(index_min, index_max):
                                    for b in range1(a+1, index_max):
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
                        for c in range1(index_min, index_max):
                            for d in range1(c+1, index_max):
                                for a in range1(index_min, index_max):
                                    for b in range1(a+1, index_max):
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
                        for c in range1(index_min, index_max):
                            for d in range1(c, index_max):
                                for a in range1(index_min, index_max):
                                    for b in range1(a+1, index_max):
                                        globals()[var_name][c, d, a, b] = var(
                                            "".join([var_name, str(c), str(d),
                                                     str(a), str(b)]))
                else:
                    raise Exception("mixed symmetry of %s undefined yet!!!" %
                                    var_name)

            else:
                raise Exception("symmetry of four-index %s undefined yet!!!" %
                                var_name)

        # -----------
        # other cases
        # -----------
        else:
            raise Exception("symmetry of %s undefined yet!!!" % var_name)

    # ============================
    # tensor case without symmetry
    # ============================
    else:
        globals()[var_name] = manifd.tensor_field(n_contravariant, n_covariant,
                                                  name=var_name)

    # add to export list
    __all__.append(var_name)
