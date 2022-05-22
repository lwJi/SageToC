# Nmesh.py
# (c) Liwei Ji 05/2022

import sys
sys.path.append('..')
import SageToC as Sg # noqa
from misc_functions import ManipulateMode as mmode # noqa


def print_component_initialization(mode, comp_info):
    var_name = comp_info.getVar_name()
    [str_name, str_varlistIndex] = comp_info.getStr_name_varlistIndex()
    buf = "double *" + str_name
    # different modes
    if(mode.value == mmode.print_comp_init_vlr_independent.value):
        buf += " = Vard(node, Vind(vlr, " + Sg.project + "->i_"
        buf += var_name.replace("dt", "") + get_init_comp(comp_info)
        if(str_varlistIndex != '0'):
            buf += " + " + str_varlistIndex
        buf += "));\n"
    elif(mode.value == mmode.print_comp_init_vlr_continuous.value):
        buf += " = Vard(node, Vind(vlr, " + str_varlistIndex + "));\n"
    elif(mode.value == mmode.print_comp_init_vlu_independent.value):
        buf += " = Vard(node, Vind(vlu, " + Sg.project + "->i_"
        buf += var_name + get_init_comp(comp_info)
        if(str_varlistIndex != '0'):
            buf += " + " + str_varlistIndex
        buf += "));\n"
    elif(mode.value == mmode.print_comp_init_vlu_continuous.value):
        buf += " = Vard(node, Vind(vlu, " + str_varlistIndex + "));\n"
    elif(mode.value == mmode.print_comp_init_more_input_output.value):
        buf += " = Vard(node, i"
        buf += var_name + get_init_comp(comp_info)
        if(str_varlistIndex != '0'):
            buf += " + " + str_varlistIndex
        buf += ");\n"
    else:
        raise Exception("print initialization mode undefined for %s!",
                        str_name)
    # write to file
    with open(Sg.cfilename, "a") as cf:
        cf.write(buf)


def get_init_comp(comp_info):
    initial_cIndex = ""
    for i in range(comp_info.getIndex_length()):
        if(comp_info.is_3d_aIndex(i)):
            initial_cIndex += "x"
        else:
            initial_cIndex += "t"
    return initial_cIndex


def print_to_cfile(buf=""):
    buf += "\n"
    with open(Sg.cfilename, "a") as cf:
        cf.write(buf)
