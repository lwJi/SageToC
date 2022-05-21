# misc_functions.py
# (c) Liwei Ji 05/2022

import enum
import re


#########
# enums #
#########

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


###########
# classes #
###########

class VarLine:

    def __init__(self, var):
        self.delim_info = ', '
        self.delim_name = '['
        # main variables
        self.infos = var.split(self.delim_info)
        self.names = self.infos[0].split(self.delim_name)

    def get_details(self):
        # interface
        name = self.names[0]
        n_contravariant = 0
        n_covariant = 0
        sym_tuple = None
        antisym_tuple = None
        aIndex_list = []
        # temp variables
        symm_list = []
        # get abstract index list
        aIndex = re.search(r'\[.*?\]', self.infos[0]).group(0).strip('[]')
        if(len(aIndex) > 0):
            aIndex_list = aIndex.split(',')
        # get symmetry list
        if(len(self.infos) == 1):
            pass
        elif(len(self.infos) == 2):
            symm_list = [self.infos[1]]
        elif(len(self.infos) == 3):
            symm_list = [self.infos[1], self.infos[2]]
        else:
            raise Exception("symm_list of %s undefined yet!!!" % name)
        # set n_covariant and n_contravariant
        for index in aIndex_list:
            if '-' in index:
                n_covariant += 1
            else:
                n_contravariant += 1
        # set sym_tuple and antisym_tuple
        if(len(symm_list) == 0):
            pass
        elif(len(symm_list) < 3):
            # go over different types of symmetries
            for symmetry in symm_list:
                symmetry_type = symmetry.split('[')[0]
                # go over different groups of same type of symmetry
                for sublist in re.findall(r'\{.*?\}', symmetry):
                    symmetry_indexlist = sublist.strip('{}').split(',')
                    if(symmetry_type == 'sym'):
                        if(sym_tuple is None):
                            sym_tuple = tuple(
                                [int(i) for i in symmetry_indexlist])
                        else:
                            if(isinstance(sym_tuple, list)):
                                sym_tuple.append(tuple(
                                    [int(i) for i in symmetry_indexlist]))
                            else:
                                sym_tuple = [sym_tuple, tuple(
                                    [int(i) for i in symmetry_indexlist])]
                    if(symmetry_type == 'antisym'):
                        if(antisym_tuple is None):
                            antisym_tuple = tuple(
                                [int(i) for i in symmetry_indexlist])
                        else:
                            if(isinstance(antisym_tuple, list)):
                                antisym_tuple.append(tuple(
                                    [int(i) for i in symmetry_indexlist]))
                            else:
                                antisym_tuple = [
                                    antisym_tuple, tuple(
                                        [int(i) for i in symmetry_indexlist])]
        else:
            raise Exception("symmetry type of %s undefined yet!!!" % name)
            # print("sym_tuple = ", sym_tuple,
            #       " antisym_tuple = ", antisym_tuple)

        return [name, n_contravariant, n_covariant, sym_tuple, antisym_tuple,
                aIndex_list]

    def prefix_of(self, value):
        var_name = "".join([value, self.names[0]])
        fullname = self.delim_name.join([var_name, self.names[1]])
        return self.delim_info.join(
            [v for vlist in [[fullname], self.infos[1:]] for v in vlist])


#############
# functions #
#############

# redefine range
def range1(start, end):
    return range(start, end+1)


# return bool: check if the abstract index is a 3D index or not:
#  4D: a,b,...,h,h1,h2,h... ,
#  3D: i,j,...,z,z1,z2,z... .
def is_3d_aIndex(aIndex):
    if(len(aIndex) > 0):
        if(ord(aIndex.replace("-", "")[0]) >= ord('i')):
            return True
        else:
            return False
    else:
        raise Exception("no abstract index!!!")


# return bool: check if this component index is a 4d index in 3d tensor
# (from abstrct index)
def is_4d_cIndex_in_3d_aIndex(aIndex, cIndex):
    return is_3d_aIndex(aIndex) and cIndex == 0
