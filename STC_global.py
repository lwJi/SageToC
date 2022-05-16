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
def STC_set_tensor(absIndex, var_name, symmetry):
    index_min = 0
    index_max = 3
    n_covariant = 0
    n_contravariant = 0
    absIndex_list = None

    # set n_convariant and n_contravariant
    if(len(absIndex) > 0):
        absIndex_list = absIndex.split(',')
        for index in absIndex_list:
            if '-' in index:
                n_covariant += 1
            else:
                n_contravariant += 1
    n_total = n_contravariant+n_covariant
    print("tensor type: (", n_covariant, ", ", n_contravariant, ") = ",
          n_total)

    # ===========
    # scalar case
    # ===========
    if(n_total == 0):
        globals()[var_name] = manifd.scalar_field(var(var_name), name=var_name)

    # =========================
    # tensor case with symmetry
    # =========================
    elif(symmetry):
        sym_type = symmetry.split('[')[0]
        sym_lists = re.findall(r'\{.*?\}', symmetry)

        # ----------------
        # two indexes case
        # ----------------
        if(n_total == 2):
            if(sym_type == 'Symmetric'):
                globals()[var_name] = manifd.tensor_field(n_contravariant,
                                                          n_covariant,
                                                          name=var_name,
                                                          sym=(0, 1))
                for a in range1(index_min, index_max):
                    for b in range1(a, index_max):
                        globals()[var_name][a, b] = var("".join(
                            [var_name, str(a), str(b)]))

            elif(sym_type == 'Antisymmetric'):
                globals()[var_name] = manifd.tensor_field(n_contravariant,
                                                          n_covariant,
                                                          name=var_name,
                                                          antisym=(0, 1))
                for a in range1(index_min, index_max):
                    for b in range1(a+1, index_max):
                        globals()[var_name][a, b] = var("".join(
                            [var_name, str(a), str(b)]))

            else:
                raise Exception("symmetry of %s undefined yet!!!" % var_name)

        # ------------------
        # three indexes case
        # ------------------
        elif(n_total == 3):
            sym_list = sym_lists[0].strip('{}').split(',')
            # c(ab) or c[ab]
            if(sym_list[0] == absIndex_list[1] and
               sym_list[1] == absIndex_list[2]):
                if(sym_type == 'Symmetric'):
                    globals()[var_name] = manifd.tensor_field(n_contravariant,
                                                              n_covariant,
                                                              name=var_name,
                                                              sym=(1, 2))
                    for c in range1(index_min, index_max):
                        for a in range1(index_min, index_max):
                            for b in range1(a, index_max):
                                globals()[var_name][c, a, b] = var("".join(
                                    [var_name, str(c), str(a), str(b)]))
                elif(sym_type == 'Antisymmetric'):
                    globals()[var_name] = manifd.tensor_field(n_contravariant,
                                                              n_covariant,
                                                              name=var_name,
                                                              antisym=(1, 2))
                    for c in range1(index_min, index_max):
                        for a in range1(index_min, index_max):
                            for b in range1(a+1, index_max):
                                globals()[var_name][c, a, b] = var("".join(
                                    [var_name, str(c), str(a), str(b)]))
                else:
                    raise Exception("symmetry of %s undefined yet!!!" %
                                    var_name)

            # (ab)c or [ab]c
            if(sym_list[0] == absIndex_list[0] and
               sym_list[1] == absIndex_list[1]):
                if(sym_type == 'Symmetric'):
                    globals()[var_name] = manifd.tensor_field(n_contravariant,
                                                              n_covariant,
                                                              name=var_name,
                                                              sym=(0, 1))
                    for a in range1(index_min, index_max):
                        for b in range1(a, index_max):
                            for c in range1(index_min, index_max):
                                globals()[var_name][a, b, c] = var("".join(
                                    [var_name, str(a), str(b), str(c)]))
                elif(sym_type == 'Antisymmetric'):
                    globals()[var_name] = manifd.tensor_field(n_contravariant,
                                                              n_covariant,
                                                              name=var_name,
                                                              antisym=(0, 1))
                    for a in range1(index_min, index_max):
                        for b in range1(a+1, index_max):
                            for c in range1(index_min, index_max):
                                globals()[var_name][a, b, c] = var("".join(
                                    [var_name, str(a), str(b), str(c)]))
                else:
                    raise Exception("symmetry of %s undefined yet!!!" %
                                    var_name)

        # -----------------
        # four indexes case
        # -----------------
        elif(n_total == 4):
            print("absindex = ", absIndex_list, "sym_lists = ", sym_lists)
            print("len(sym_lists) = ", len(sym_lists))

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
