#!/usr/bin/env sage -python

##################
# import modules #
##################
from sage.all import Manifold # noqa
import os
import sys
sys.path += ['..', '../Codes']
import SageToC as Sg # noqa
import Nmesh # noqa
from Nmesh import print_to_cfile as pr # noqa
from misc_functions import ManipulateMode as mmode # noqa

# Parallelism().set(nproc=4)


##########################
# dimension and manifold #
##########################
Sg.dimens = 3
Sg.manifd = Manifold(Sg.dimens, name='M', latex_name=r'\mathcal{M}',
                     structure="Lorentzian", start_index=0)
Sg.manifd.set_calculus_method('sympy')

# coordinats
# cartesian.<T, X, Y, Z> = Sg.manifd.chart('t:(0,+oo) x y z:(-oo,+oo)')
# cartesian.<X, Y, Z> = Sg.manifd.chart('x y z:(-oo,+oo)')
cartesian = Sg.manifd.chart('x y z:(-oo,+oo)')


##################
# variable lists #
##################
evolution = [
    "u[i]"
]
temporary = [
    "v[i]"
]
moreinput = [
    "M[i,-j], sym[{0,1}]"
    # "alpha[]"
    # "N[k,l], antisym[{0,1}]",
    # "Phi[-k,-a,-b], sym[{1,2}]",
    # "ddg[-k,-l,-a,-b], antisym[{0,1},{2,3}]",
    # "ddg2[-k,-l,-a,-b], sym[{0,1}], antisym[{2,3}]"
]

# set up variable lists
Evol = Sg.EvolutionVarlist(evolution)
dtEvol = Evol.prefix()
Temp = Sg.TemporaryVarlist(temporary)
MoreInput = Sg.MoreInputVarlist(moreinput)


##############
# defint rhs #
##############
# update the names (since its a cope from module Sg)
from SageToC import M, u, v # noqa

Sg.v_rhs = M(u)
Sg.u_rhs_Msqr = M(v)
Sg.u_rhs_otherwise = v


##################
# print to files #
##################
Sg.cfilename = "test.c"
Sg.project = "ADM"
if os.path.exists(Sg.cfilename):
    os.remove(Sg.cfilename)
# set function of printing component initialization
Sg.print_component_initialization = Nmesh.print_component_initialization

# start writing
pr("/* " + Sg.cfilename + " */")
pr("/* (c) Liwei Ji 05/2022 */")
pr("/* Produced with SageToC.py */")
pr()
pr("extern t" + Sg.project + " " + Sg.project + "[1]")
pr()
pr("void test(tVarList *vlu, tVarList *vlr)")
pr("{")
pr("tMesh *mesh = u->mesh;")
pr("int Msqr = GetvLax(Par(\"ADM_ConstraintNorm\"), \"Msqr\");")
pr()
pr("formylnodes(mesh)")
pr("{")
pr("tNode *node = MyLnode;")
pr("int ijk;")
pr()
pr("forpoints(node, ijk)")
pr("{")
pr("int iMxx = Ind(\"ADM_gxx\");")
pr()
dtEvol.printInit()
Evol.printInit()
MoreInput.printInit()
pr()
Temp.printEqn()
pr()
pr("if(Msqr) {")
pr()
dtEvol.printEqn(mmode.print_comp_eqn_primary_with_suffix, "_Msqr")
pr()
pr("} else {")
pr()
dtEvol.printEqn(mmode.print_comp_eqn_primary_with_suffix, "_otherwise")
pr()
pr("}")
pr()
pr("} /* end of points */")
pr("} /* end of nodes */")
pr("}")
