# noqa: E402

# Nmesh.py
# (c) Liwei Ji 05/2022

import _paths # noqa
import SageToC as Sg
from misc_functions import ManipulateMode as mmode


def print_comp_initialization(mode, var_name, aIndex_list,
                              str_name, str_varlistIndex):
    buf = "double *" + str_name
    # different modes
    if(mode.value == mmode.print_comp_init_vlr_independent.value):
        buf += " = Vard(node, Vind(vlr, " + Sg.project + "->i_"
        buf += var_name.replace("dt", "")
        buf += get_init_comp(aIndex_list) + str_varlistIndex
        buf += "));\n"
    elif(mode.value == mmode.print_comp_init_vlr_continuous.value):
        buf += " = Vard(node, Vind(vlr, " + str_varlistIndex + "));\n"
    elif(mode.value == mmode.print_comp_init_vlu_independent.value):
        buf += " = Vard(node, Vind(vlu, " + Sg.project + "->i_"
        buf += var_name
        buf += get_init_comp(aIndex_list) + str_varlistIndex
        buf += "));\n"
    elif(mode.value == mmode.print_comp_init_vlu_continuous.value):
        buf += " = Vard(node, Vind(vlu, " + str_varlistIndex + "));\n"
    elif(mode.value == mmode.print_comp_init_more_input_output.value):
        buf += " = Vard(node, Vind(vlu, i"
        buf += var_name
        buf += get_init_comp(aIndex_list) + str_varlistIndex
        buf += "));\n"
    else:
        raise Exception("print initialization mode undefined for %s!",
                        str_name)
    # write to file
    with open(Sg.cfilename, "a") as cf:
        cf.write(buf)


def get_init_comp(aIndex_list):
    return "tt"


def print_to_cfile(buf=""):
    buf += "\n"
    with open(Sg.cfilename, "a") as cf:
        cf.write(buf)
