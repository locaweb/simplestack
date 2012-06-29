import re

def not_implemented(f):
    def wrapped(*args, **kws):
        try:
            print("NEW METHOD")
            return f(*args, **kws)
        except:
            print("FODEU")
    return wrapped

class not_implemented_all(object):
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
                setattr(self.subject, old_method_name, not_implemented(old_method))

@not_implemented_all
class Abc(object):
    def __init__(self):
        pass

    def hello(self):
        print "OLA"

    def ola(self):
        print "XUPA"

a = Abc()

a.hello()
a.ola()
