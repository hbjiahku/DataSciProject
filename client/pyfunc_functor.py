class Functor(object):
    def __init__(self, funct):
        self.funct = funct

    def __call__(self, *args, **kwargs):
        return self.funct(*args, **kwargs)


def reload_interface(functor_d):
    for fname in functor_d:
        globals()[fname] = Functor(functor_d[fname])
