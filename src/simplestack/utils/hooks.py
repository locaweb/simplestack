import re

class hook_all(object):
    def __init__(self, subject):
        self.subject = subject
        self.regex = r'^[^_]'
        self.__redefine_clazz__()

    def __call__(self, *args, **kws):
        return self.subject(*args, **kws)

    def __redefine_clazz__(self):
        instancemethod = type(self.__redefine_clazz__)
        for old_method_name in dir(self.subject):
            old_method = getattr(self.subject, old_method_name)
            if type(old_method) is instancemethod and re.match(self.regex, old_method_name):
                setattr(self.subject, old_method_name, self.hook(old_method))

def not_implemented(f):
    def wrapped(*args, **kws):
        # ADD CODE HERE
        f_self = args[0]
        print(f_self.attr)
        print("NEW METHOD")
        return f(*args, **kws)
    return wrapped

class not_implemented_all(hook_all):
    def __init__(self, subject):
        self.hook = not_implemented
        super(self.__class__, self).__init__(subject)

@not_implemented_all
class Abc(object):
    def __init__(self):
        self.attr = "an attribute"

    def hello(self):
        print "HELLO"

    def ola(self):
        print "OLA"

a = Abc()
a.hello()
a.ola()
