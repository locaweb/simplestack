# Copyright 2012 Locaweb.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
# @author: Francisco Freire, Locaweb.
# @author: Thiago Morello (morellon), Locaweb.
# @author: Willian Molinari (PotHix), Locaweb.

import re

from simplestack.exceptions import FeatureNotImplemented


class hook_all(object):
    def __init__(self, subject):
        self.subject = subject
        self.__redefine_clazz__()

    def __call__(self, *args, **kws):
        return self.subject(*args, **kws)

    def __redefine_clazz__(self):
        instancemethod = type(self.__redefine_clazz__)
        for old_method_name in dir(self.subject):
            old_method = getattr(self.subject, old_method_name)
            is_a_match = re.match(self.regex, old_method_name)
            if type(old_method) is instancemethod and is_a_match:
                setattr(self.subject, old_method_name, self.hook(old_method))


def not_implemented(f):
    def wrapped(*args, **kws):
        f_self = args[0]
        if not (hasattr(f_self, "libvirt_connection") and
                f_self.libvirt_connection):
            raise FeatureNotImplemented()
        return f(*args, **kws)
    return wrapped


class not_implemented_all(hook_all):
    def __init__(self, subject):
        self.hook = not_implemented
        self.regex = r'^(pool|guest|media|network|snapshot|tag)'
        super(self.__class__, self).__init__(subject)


@not_implemented_all
class Mock(object):
    def __init__(self):
        pass

    def pool_stuff(self):
        pass

mock = Mock()
try:
    mock.pool_stuff()
except Exception, e:
    print e
