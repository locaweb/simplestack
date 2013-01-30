# Copyright 2013 Locaweb.
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
# @author: Willian Molinari (PotHix), Locaweb.

from simplestack.exceptions import FeatureNotImplemented


def libvirt(available):
    """
    Decide if it should raise FeatureNotImplemented for if
    the current method is not using libvirt

    Unfortulately is not possible to get self.libvirt_connection here
    """
    def wrapper(f):
        def has_connection(*args, **kwargs):
            if not available:
                raise FeatureNotImplemented()
            return f(*args, **kwargs)

        return has_connection
    return wrapper
