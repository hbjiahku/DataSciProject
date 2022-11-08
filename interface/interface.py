import os
import inspect
import io
import keyword

from client.rest_proxy import funct_call
from dev.main import *  # Warning: this is used to import the dev functions, don't delete.
from constant import *

__funct_call = funct_call

FUNC = {}


def filtered_fname(fname):
    for nnn in ["md_"]:  # Remember add prefix here when add new shared module.
        if fname.startswith(nnn):
            return True
    return False


def get_interface():
    def conv_inspect_empty(vvv):
        if vvv.default is vvv.empty:
            return None
        else:
            return vvv.default

    global FUNC
    for kkk in globals():
        if filtered_fname(kkk):
            FUNC[kkk] = globals()[kkk]

    interface = {}
    for fname in FUNC:
        fff = FUNC[fname]
        param_list = []
        param = inspect.signature(fff).parameters
        for pn in param:
            param_list.append([pn, conv_inspect_empty(param[pn])])
        interface[fname] = {
            "param": param_list,
            "doc": inspect.getdoc(fff)
        }
    return interface


def load_interface(debug_file=True, server_side=False):
    interface_d = get_interface()
    py_file = io.StringIO()
    if server_side:
        print(f"from dev.main import *", file=py_file)
    else:
        print("from interface.interface import __funct_call", file=py_file)
    print("", file=py_file)
    print("", file=py_file)
    for fname in interface_d:
        input_param = []
        for p in interface_d[fname]["param"]:
            arg = str(p[0])
            if len(p) > 1:
                default = str(p[1])
                if not (keyword.iskeyword(default) or default.isnumeric()):
                    default = "\"%s\"" % default
                input_param.append(arg + "=" + default)
            else:
                input_param.append(arg)
        print("def %s(%s):" % (SYS_NAME + "_" + fname, ", ".join(input_param)), file=py_file)
        print("\t\"\"\"%s\"\"\"" % (interface_d[fname]["doc"]), file=py_file)
        output_param = ["=".join(map(str, [p[0], p[0]])) for p in interface_d[fname]["param"]]
        if server_side:
            args_str = ",".join(output_param)
            print(f"\treturn {fname}({args_str})", file=py_file)
        else:
            print("\timport os", file=py_file)
            print("\tprint(os.getcwd())", file=py_file)
            print("\tprint(globals())", file=py_file)
            print("\treturn __funct_call(%s)" % ", ".join([f"\"{SYS_NAME + '_' + fname}\""] + output_param), file=py_file)

        print("", file=py_file)
    functor_d = {}
    if server_side:
        debug_path = r"\server\py_debug.py"
    else:
        debug_path = r"\client\py_debug.py"
    if debug_file:
        print("# This is debug file.", file=py_file)
        with open(PROJECT_ROOT + debug_path, "w") as f:
            f.write(py_file.getvalue())
    else:
        exec(py_file.getvalue(), globals(), functor_d)

    return functor_d


if __name__ == "__main__":
    functor_d = get_interface()
    load_interface(debug_file=True, server_side=True)
    load_interface(debug_file=True, server_side=False)
