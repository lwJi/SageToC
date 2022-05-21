# STC_global.py
# (c) Liwei Ji 05/2022

from sage.calculus.var import var
import misc_functions as mf
from misc_functions import range1 as rg1
from misc_functions import ManipulateMode as mmode

print('Welcome to SageToC (a code generator)')


####################
# global variables #
####################

# dimension
dimens = None

# manifold name
manifd = None

# dict between component and varlist
map_component_to_varlist = []

# if new varlist
bool_new_varlist = True

# grid index
grid_index = "[ijk]"

# dt prefix
prefix_of_dt = "dt"
# suffix of rhs name when there is a if statement
suffix_of_rhs = ""

# output filename
project = "Project"
cfilename = "output.c"


# for simple export
__all__ = []


###########################
# SageToC varlist classes #
###########################

class Varlist:

    def __init__(self, varlist):
        self.varlist = varlist
        self.varlist_info = []
        # define tensor
        for var_info in self.varlist:
            # get var infos
            [var_name, n_contravariant, n_covariant, sym_tuple, antisym_tuple,
             aIndex_list] = mf.VarLine(var_info).get_details()
            n_total = n_contravariant + n_covariant
            self.varlist_info.append([var_name, n_total,
                                      sym_tuple, antisym_tuple, aIndex_list])
            # define Sage tensor
            define_tensors(var_name, n_contravariant, n_covariant,
                           sym_tuple, antisym_tuple)
            print("defining ", var_name, "...")

    def getVar_name(self, i):
        return self.varlist_info[i][0]

    def getN_total(self, i):
        return self.varlist_info[i][1]

    def getSym_tuple(self, i):
        return self.varlist_info[i][2]

    def getAntisym_tuple(self, i):
        return self.varlist_info[i][3]

    def getaIndex_list(self, i):
        return self.varlist_info[i][4]

    def maniComponents(self, mode, suffix=None):
        print("mode = ", mode.name)
        # consider suffix
        if(suffix is not None):
            global suffix_of_rhs
            suffix_of_rhs = suffix
        # reset bool_new_varlist
        global bool_new_varlist
        bool_new_varlist = True
        # manipulate vars: set/print
        for i in range(len(self.varlist)):
            manipulate_components(
                mode, self.getVar_name(i), self.getN_total(i),
                self.getSym_tuple(i), self.getAntisym_tuple(i),
                self.getaIndex_list(i))

    def prefix(self, value=None, mode=None):
        dt_varlist = []
        if(value is None):
            value = prefix_of_dt
        # construct list of vars with prefix 'value'
        for var_info in self.varlist:
            dt_varlist.append(mf.VarLine(var_info).prefix_of(value))
        return dtEvolutionVarlist(dt_varlist, mode)


class EvolutionVarlist(Varlist):
    def __init__(self, varlist, mode=None):
        Varlist.__init__(self, varlist)
        if(mode is None):
            mode = mmode.set_comp_gf_independent
        self.maniComponents(mode)

    def printInit(self, mode=None):
        if(mode is None):
            mode = mmode.print_comp_init_vlu_independent
        self.maniComponents(mode)


class dtEvolutionVarlist(Varlist):
    def __init__(self, varlist, mode=None):
        Varlist.__init__(self, varlist)
        if(mode is None):
            mode = mmode.set_comp_gf_independent
        self.maniComponents(mode)

    def printInit(self, mode=None):
        if(mode is None):
            mode = mmode.print_comp_init_vlr_independent
        self.maniComponents(mode)

    def printEqn(self, suffix=None, mode=None):
        if(mode is None):
            mode = mmode.print_comp_eqn_primary
        self.maniComponents(mode, suffix)


class MoreInputVarlist(Varlist):
    def __init__(self, varlist, mode=None):
        Varlist.__init__(self, varlist)
        if(mode is None):
            mode = mmode.set_comp_gf_independent
        self.maniComponents(mode)

    def printInit(self, mode=None):
        if(mode is None):
            mode = mmode.print_comp_init_more_input_output
        self.maniComponents(mode)


class MoreOutputVarlist(Varlist):
    def __init__(self, varlist, mode=None):
        Varlist.__init__(self, varlist)
        if(mode is None):
            mode = mmode.set_comp_gf_independent
        self.maniComponents(mode)

    def printInit(self, mode=None):
        if(mode is None):
            mode = mmode.print_comp_init_more_input_output
        self.maniComponents(mode)

    def printEqn(self, suffix=None, mode=None):
        if(mode is None):
            mode = mmode.print_comp_eqn_primary
        self.maniComponents(mode, suffix)


class TemporaryVarlist(Varlist):
    def __init__(self, varlist, mode=None):
        Varlist.__init__(self, varlist)
        if(mode is None):
            mode = mmode.set_comp_temp
        self.maniComponents(mode)

    def printEqn(self, suffix=None, mode=None):
        if(mode is None):
            mode = mmode.print_comp_eqn_temp
        self.maniComponents(mode, suffix)


####################
# global functions #
####################

# which should be defined in Codes/app.py
def print_comp_initialization(mode, var_name, aIndex_list,
                              str_name, str_varlistIndex):
    raise Exception("print_component_initialization() undefined!")


def print_component_initialization(mode, var_name, aIndex_list, cIndex_list):
    str_name = str(
        globals()[var_name][tuple(cIndex_list)].expr()).replace("_ijk_", "")
    str_varlistIndex = str(map_component_to_varlist[
        [i[0] for i in
         map_component_to_varlist].index(str_name.replace("_ijk_", ""))][1])
    print_comp_initialization(mode, var_name, aIndex_list,
                              str_name, str_varlistIndex)


def print_component_equation(mode, var_name, cIndex_list):
    expr_name = globals()[var_name][tuple(cIndex_list)].expr()
    # different modes
    if(mode.value == mmode.print_comp_eqn_primary.value or
       mode.value == mmode.print_comp_eqn_add_to_primary.value):
        rhss_name = globals()[var_name.replace(prefix_of_dt, "", 1)+"_rhs"][
            tuple(cIndex_list)].expr()
    elif(mode.value == mmode.print_comp_eqn_primary_with_suffix.value):
        rhss_name = globals()[
            var_name.replace(prefix_of_dt, "", 1)+suffix_of_rhs+"_rhs"][
            tuple(cIndex_list)].expr()
    elif(mode.value == mmode.print_comp_eqn_temp.value):
        rhss_name = globals()[var_name+"_rhs"][tuple(cIndex_list)].expr()
    else:
        raise Exception("print equation mode undefined yet for %s!", var_name)
    # tranform to string
    lhs_str = str(expr_name).replace("_ijk_", grid_index)
    rhs_str = str(rhss_name).replace("_ijk_", grid_index)
    # write to file
    with open(cfilename, "a") as cf:
        if(mode.value == mmode.print_comp_eqn_add_to_primary.value):
            cf.write(lhs_str + " +=\n")
        elif(mode.value == mmode.print_comp_eqn_temp.value):
            cf.write("double " + lhs_str + " =\n")
        else:
            cf.write(lhs_str + " =\n")
        cf.write(rhs_str + ";\n\n")


def print_component(mode, var_name, aIndex_list, cIndex_list):
    if(mmode.print_comp_init.name in mode.name):
        print_component_initialization(mode, var_name, aIndex_list,
                                       cIndex_list)
    if(mmode.print_comp_eqn.name in mode.name):
        print_component_equation(mode, var_name, cIndex_list)


def set_component_and_register_to_indexmap(mode, var_name, cIndex_list):
    global bool_new_varlist
    index_tuple = tuple(cIndex_list)
    if(dimens == 4):
        comp_name = "".join(
            [n for nlist in [[var_name], [str(index) for index in cIndex_list]]
             for n in nlist])
    else:
        comp_name = "".join(
            [n for nlist in [[var_name],
                             [str(index+1) for index in cIndex_list]]
             for n in nlist])
    if(mode.value == mmode.set_comp_temp.value):
        fullname = comp_name
    else:
        fullname = "".join([comp_name, "_ijk_"])

    if(len(map_component_to_varlist) == 0 or
       bool_new_varlist or  # for 'continuous varlist index case'
       (mode.value == mmode.set_comp_gf_independent.value and
            var_name != map_component_to_varlist[-1][0][0:len(var_name)])):
        varlist_index = 0
    else:
        varlist_index = map_component_to_varlist[-1][1] + 1

    # register to global index dictionary
    map_component_to_varlist.append([comp_name, varlist_index])
    # set component
    if(len(cIndex_list) == 0):  # scalar case
        # globals()[var_name].add_expr(var(var_name))
        pass
    else:  # tensor case
        globals()[var_name][index_tuple] = var(fullname)

    bool_new_varlist = False


# different modes
def manipulate_component(mode, var_name, aIndex_list, cIndex_list):
    # set/skip 4d compoents for 3d tensor

    # set/print components
    if(mmode.set_comp.name in mode.name):  # set components ...
        set_component_and_register_to_indexmap(mode, var_name, cIndex_list)
    elif(mmode.print_comp.name in mode.name):  # print components ...
        print_component(mode, var_name, aIndex_list, cIndex_list)
    else:
        raise Exception("manipulate component undefined for var %s!!!",
                        var_name)


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


# manipulate components
def manipulate_components(mode, var_name, n_total, sym_tuple, antisym_tuple,
                          aIndex_list):
    index_min = 0
    index_max = dimens-1

    def mani_component_value(cIndex_list):
        manipulate_component(mode, var_name, aIndex_list, cIndex_list)

    # scalar case
    if(n_total == 0):
        mani_component_value([])

    # tensor case without symmetry
    elif(sym_tuple is None and antisym_tuple is None):
        if(n_total == 1):
            for a in rg1(index_min, index_max):
                mani_component_value([a])
        elif(n_total == 2):
            for a in rg1(index_min, index_max):
                for b in rg1(index_min, index_max):
                    mani_component_value([a, b])
        elif(n_total == 3):
            for c in rg1(index_min, index_max):
                for a in rg1(index_min, index_max):
                    for b in rg1(index_min, index_max):
                        mani_component_value([c, a, b])
        elif(n_total == 4):
            for c in rg1(index_min, index_max):
                for d in rg1(index_min, index_max):
                    for a in rg1(index_min, index_max):
                        for b in rg1(index_min, index_max):
                            mani_component_value([c, d, a, b])
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
                        mani_component_value([a, b])
            # [ab]
            elif(antisym_tuple is not None):
                for a in rg1(index_min, index_max):
                    for b in rg1(a+1, index_max):
                        mani_component_value([a, b])
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
                                mani_component_value([c, a, b])
                # (ab)c
                elif(sym_tuple[0] == 0 and sym_tuple[1] == 1):
                    for a in rg1(index_min, index_max):
                        for b in rg1(a, index_max):
                            for c in rg1(index_min, index_max):
                                mani_component_value([a, b, c])
                else:
                    raise Exception("sym of %s undefined yet!!!" %
                                    var_name)
            elif(sym_tuple is None and antisym_tuple is not None):
                # c[ab]
                if(antisym_tuple[0] == 1 and antisym_tuple[1] == 2):
                    for c in rg1(index_min, index_max):
                        for a in rg1(index_min, index_max):
                            for b in rg1(a+1, index_max):
                                mani_component_value([c, a, b])
                # [ab]c
                elif(antisym_tuple[0] == 0 and antisym_tuple[1] == 1):
                    for a in rg1(index_min, index_max):
                        for b in rg1(a+1, index_max):
                            for c in rg1(index_min, index_max):
                                mani_component_value([a, b, c])
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
                                        mani_component_value([c, d, a, b])
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
                                        mani_component_value([c, d, a, b])
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
                                        mani_component_value([c, d, a, b])
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
                                        mani_component_value([c, d, a, b])
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
                                        mani_component_value([c, d, a, b])
                else:
                    raise Exception("mixed symmetry of %s undefined yet!!!" %
                                    var_name)

            else:
                raise Exception("symmetry of four-index %s undefined yet!!!" %
                                var_name)

        # other num of indexes case
        else:
            raise Exception("symmetry of %s undefined yet!!!" % var_name)
