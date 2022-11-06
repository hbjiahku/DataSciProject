# This file is used to start the client (connect and initialize the interface)
from interface.interface import load_interface
from client.pyfunc_functor import reload_interface

functor_d = load_interface(debug_file=False, server_side=False)
reload_interface(functor_d)

# import client.py_debug as py_debug # debug
from client.py_exe import pyfunc_caller
