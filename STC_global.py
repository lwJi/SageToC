# STC_global.py
# (c) Liwei Ji 05/2022

####################
# global variables #
####################

# dimension
dim = 0

# manifold name
manifd = None


# set tensors
def set_tensors(contravariant, covariant, var_name):
    globals()[var_name] = manifd.tensor_field(contravariant, covariant,
                                              name=var_name)
