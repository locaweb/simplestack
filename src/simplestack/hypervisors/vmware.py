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

from pysphere import VIServer
from simplestack.utils import vmware
from simplestack.exceptions import EntityNotFound
from simplestack.hypervisors.base import SimpleStack

import re
import datetime
import pysphere


class Stack(SimpleStack):

    state_translation = {
        "POWERED ON": "STARTED",
        "POWERED OFF": "STOPPED",
        "SUSPENDED": "PAUSED"
    }

    def __init__(self, poolinfo):
        self.connection = False
        self.poolinfo = poolinfo
        self.connect()

    def connect(self):
        self.connection = VIServer()
        self.connection.connect(
            self.poolinfo.get("api_server"),
            self.poolinfo.get("username"),
            self.poolinfo.get("password")
        )
        return

    def pool_info(self):
        return {
            "master": self.poolinfo.get("api_server")
        }

    def guest_list(self):
        return [
            {"id": self.connection.get_vm_by_path(path).properties.name}
            for path in self.connection.get_registered_vms(
                cluster=self.poolinfo.get('cluster')
            )
        ]

    def guest_info(self, guest_id):
        vm = self._vm_ref(guest_id)
        return self._vm_info(vm)

    def guest_shutdown(self, guest_id, force=False):
        vm = self._vm_ref(guest_id)
        if force:
            return vm.power_off()
        else:
            return vm.shutdown_guest()

    def guest_start(self, guest_id):
        vm = self._vm_ref(guest_id)
        return vm.power_on()

    def guest_reboot(self, guest_id, force=False):
        vm = self._vm_ref(guest_id)
        if force:
            return vm.reset()
        else:
            return vm.reboot_guest()

    def guest_suspend(self, guest_id):
        vm = self._vm_ref(guest_id)
        return vm.suspend()

    def guest_resume(self, guest_id):
        return self.guest_start(guest_id)

    def guest_update(self, guest_id, guestdata):
        vm = self._vm_ref(guest_id)
        vmware.update_vm(self.connection, vm, guestdata)
        return self._vm_info(self._vm_ref(guest_id))

    def guest_delete(self, guest_id):
        vm = self._vm_ref(guest_id)
        vmware.delete_vm(self.connection, vm)

    def snapshot_list(self, guest_id):
        vm = self._vm_ref(guest_id)
        snaps = [self._snapshot_info(s) for s in vm.get_snapshots()]
        return snaps

    def media_mount(self, guest_id, media_data):
        vm = self._vm_ref(guest_id)
        vmware.update_vm(self.connection, vm, {"iso": media_data})

    def media_info(self, guest_id):
        vm = self._vm_ref(guest_id)
        media = vmware.get_cd(vm)
        if media.connectable.connected:
            return {"name": media.backing.fileName}
        else:
            return {"name": None}

    def snapshot_create(self, guest_id, snapshot_name=None):
        if not snapshot_name:
            snapshot_name = str(datetime.datetime.now())
        vm = self._vm_ref(guest_id)
        snap = vmware.create_snapshot(self.connection, vm, snapshot_name)
        return self._snapshot_info(snap)

    def snapshot_info(self, guest_id, snapshot_id):
        vm = self._vm_ref(guest_id)
        snap = vmware.get_snapshot(vm, snapshot_id)
        if snap:
            return self._snapshot_info(snap)
        else:
            raise EntityNotFound("Snapshot", snapshot_id)

    def snapshot_revert(self, guest_id, snapshot_id):
        vm = self._vm_ref(guest_id)
        snap = vmware.get_snapshot(vm, snapshot_id)
        vmware.revert_to_snapshot(self.connection, vm, snap)

    def snapshot_delete(self, guest_id, snapshot_id):
        vm = self._vm_ref(guest_id)
        snap = vmware.get_snapshot(vm, snapshot_id)
        vmware.delete_snapshot(self.connection, vm, snap)

    def tag_list(self, guest_id):
        vm = self._vm_ref(guest_id)
        return vmware.get_tags(vm)

    def tag_create(self, guest_id, tag_name):
        vm = self._vm_ref(guest_id)
        tags = vmware.create_tag(tag_name, vm)
        vmware.update_vm(self.connection, vm, {"tags": tags})
        return tags

    def tag_delete(self, guest_id, tag_name):
        vm = self._vm_ref(guest_id)
        tags = vmware.delete_tag(tag_name, vm)
        vmware.update_vm(self.connection, vm, {"tags": tags})
        return tags

    def _vm_ref(self, vm_id):
        regex = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
        if re.match(regex, vm_id, re.I):
            return vmware.get_vm_by_uuid(self.connection, vm_id)
        else:
            return self.connection.get_vm_by_name(vm_id)

    def _vm_info(self, vm):
        vm_info = vm.get_properties()
        return {
            'id': vm.properties.config.uuid,
            'name': vm_info.get('name'),
            'cpus': vm_info.get('num_cpu'),
            'memory': vm_info.get('memory_mb'),
            'hdd': vmware.get_disk_size(vm) / (1024 * 1024),
            'tools_up_to_date': vm.properties.guest.toolsStatus == "toolsOk",
            'state': self.state_translation[vm.get_status()],
        }

    def _snapshot_info(self, snapshot):
        return {
            'id': snapshot.get_description(),
            'name': snapshot.get_name(),
            'state': snapshot.get_state(),
            'path': snapshot.get_path(),
            'created': snapshot.get_create_time()
        }
