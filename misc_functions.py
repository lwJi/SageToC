# misc_functions.py
# (c) Liwei Ji 05/2022

import enum
import re


# manipulate mode
class ManipulateMode(enum.Enum):
    set_comp = enum.auto()  # group
    set_comp_gf_independent = enum.auto()  # each var idx starts from zero
    set_comp_gf_continuous = enum.auto()  # each varlist use one long idx array
    set_comp_temp = enum.auto()  # temp var, which is not grid function
    print_comp = enum.auto()  # group
    print_comp_init = enum.auto()  # sub group
    print_comp_init_vlr_independent = enum.auto()
    print_comp_init_vlr_continuous = enum.auto()
    print_comp_init_vlu_independent = enum.auto()
    print_comp_init_vlu_continuous = enum.auto()
    print_comp_init_more_input_output = enum.auto()
    print_comp_eqn = enum.auto()  # sub group
    print_comp_eqn_temp = enum.auto()
    print_comp_eqn_primary = enum.auto()
    print_comp_eqn_add_to_primary = enum.auto()
    print_comp_eqn_primary_with_suffix = enum.auto()


# redefine range
def range1(start, end):
    return range(start, end+1)


# get var_name, n_contravariant, n_covariant, sym_tuple, anitsym_tuple
# notice the sym_tuple and antisym_tuple can be lists
def get_details(var):
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
