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
# @author: Thiago Morello (morellon), Locaweb.
# @author: Willian Molinari (PotHix), Locaweb.


class FormatView(object):

    def guest(self, vm_id, name, cpus, memory, hdd, paravirt, tools, state, host):
        return {
            'id': vm_id,
            'name': name,
            'cpus': int(cpus),
            'memory': int(memory),
            'hdd': hdd,
            'paravirtualized': paravirt,
            'tools_up_to_date': tools,
            'state': state,
            'host': host
        }

    def disk(self, disk_id, name, device, size, extra_info):
        return {
            'id': disk_id,
            'name': name,
            'number': device,
            'size': size,
            'extra_info': extra_info
        }

    def snapshot(self, snap_id, name, state=None, path=None, created=None):
        return {
            'id': snap_id,
            'name': name,
            'state': state,
            'path': path,
            'created': created

        }

    def network_interface(self, vif_id, device, mac, name_label):
        return {
            'id': vif_id,
            'number': device,
            'mac': mac,
            'network': name_label
        }

    def pool(self, used_memory, total_memory, master):
        return {
            "used_memory": used_memory,
            "total_memory": total_memory,
            "master": master
        }
