def setter(class_):
    class_.__init__(class_)
    vars_ = vars(class_).copy()
    for var in vars_:
        if not var.startswith('__') and not callable(getattr(class_, var)):
            def test(class_, arg):
                setattr(class_, var, arg)
            setattr(class_, "set_" + str(var), test)
    return class_

