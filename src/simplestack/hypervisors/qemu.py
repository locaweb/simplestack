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

from simplestack.hypervisors.base import SimpleStack

import libvirt


class Stack(SimpleStack):

    state_translation = {
        1: "STARTED",
        5: "STOPPED",
        7: "PAUSED"
    }

    def __init__(self, poolinfo):
        self.connection = False
        self.poolinfo = poolinfo
        self.connect()

    def connect(self):
        self.connection = libvirt.open("qemu://%s@%s/system" % (
            self.poolinfo.get("username"),
            self.poolinfo.get("api_server")
        ))

    def guest_list(self):
        return [
            {"id": id}
            for id in self.connection.listDomainsID()
        ]

    def guest_info(self, guest_id):
        dom = self.connection.lookupByID(guest_id)
        return self._vm_info(dom)

    def _vm_info(dom):
        infos = dom.info()
        return {
            'id': dom.ID(),
            'name': dom.name(),
            'cpus': infos[3],
            'memory': infos[1]/1024,
            'hdd': None,
            'tools_up_to_date': None,
            'state': self.state_translation[infos[0]],
        }
