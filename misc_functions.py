# misc_functions.py
# (c) Liwei Ji 05/2022

import enum


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
