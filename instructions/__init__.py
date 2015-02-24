from .commands import *

# commands package provides us with an API in it's __init__.py
# file, i.e. which names of the package should be accessible by
# the outer world. These same names should also be accessible
# within the "instructions" namespace. One way to solve the problem
# is to repeat all the imports in this file, but that violates DRY
# principles, the other way is to make a star import. The thing
# is that after a star import from the commands package we also
# have all modules of the commands package in current namespace,
# which is not what we want, so we have to delete them and clean
# our namespace.
del compounds, prototypes
