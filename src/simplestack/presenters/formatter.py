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
# @author: Thiago Morello (morellon), Locaweb.
# @author: Willian Molinari (PotHix), Locaweb.


class Formatter(object):

    def host(self, host_id, name, address):
        return {
            'id': host_id,
            'name': name,
            'address': address
        }

    def storage(self, sr_id, name, sr_type, used_space, allocated_space,
                physical_size):
        return {
            'id': sr_id,
            'name': name,
            'type': sr_type,
            'used_space': int(used_space),
            'allocated_space': int(allocated_space),
            'size': int(physical_size)
        }

    def guest(self, vmid, name, cpus, mem, hdd, pvirt, tools, ip, state, host):
        return {
            'id': vmid,
            'name': name,
            'cpus': int(cpus),
            'memory': int(mem),
            'hdd': hdd,
            'paravirtualized': pvirt,
            'tools_up_to_date': tools,
            'ip': ip,
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

    def network_interface(self, vif_id, device, mac, name_label, locking_mode, ipv4_allowed, ipv6_allowed, rate_limit=None):
        return {
            'id': vif_id,
            'number': device,
            'mac': mac,
            'locking_mode': locking_mode,
            'ipv4_allowed': ipv4_allowed,
            'ipv6_allowed': ipv6_allowed,
            'network': name_label,
            'rate_limit': rate_limit
        }

    def pool(self, used_memory, total_memory, uuid, master, software_info=None):
        return {
            "used_memory": used_memory,
            "total_memory": total_memory,
            "uuid": uuid,
            "master": master,
            "software_info": software_info
        }
