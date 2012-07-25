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

from pysphere import VIServer, VITask
from pysphere.vi_property import VIProperty
from pysphere.vi_virtual_machine import VIVirtualMachine
from pysphere.resources import VimService_services as VI

# ns0.VirtualCdromIsoBackingInfo_Def
from pysphere.resources import VimService_services_types as VITypes
from simplestack.exceptions import HypervisorError

import re
import uuid

VCdIsoBackingInfo = VITypes.ns0.VirtualCdromIsoBackingInfo_Def(None).pyclass
VirtualMachineVMIROM = VITypes.ns0.VirtualMachineVMIROM_Def(None).pyclass


def get_vm_by_uuid(server, guest_id):
    request = VI.FindByUuidRequestMsg()
    mor_search_index = request.new__this(
        server._do_service_content.SearchIndex
    )
    mor_search_index.set_attribute_type('SearchIndex')
    request.set_element__this(mor_search_index)
    request.set_element_uuid(guest_id)
    request.set_element_vmSearch(True)
    vm = server._proxy.FindByUuid(request)._returnval
    if vm is not None:
        return VIVirtualMachine(server, vm)


def update_vm(server, vm_obj, guestdata):
    new_annotation = guestdata.get("tags")
    new_cpus = guestdata.get("cpus")
    new_hdd = guestdata.get("hdd")
    new_iso = guestdata.get("iso")
    new_memory = guestdata.get("memory")
    new_name = guestdata.get("name")

    request = VI.ReconfigVM_TaskRequestMsg()
    _this = request.new__this(vm_obj._mor)
    _this.set_attribute_type(vm_obj._mor.get_attribute_type())
    request.set_element__this(_this)
    spec = request.new_spec()

    if new_name and vm_obj.properties.config.name != new_name:
        spec.set_element_name(new_name)

    if new_memory and vm_obj.properties.config.hardware.memoryMB != new_memory:
        # set the new RAM size
        spec.set_element_memoryMB(new_memory)

    if new_cpus and vm_obj.properties.config.hardware.numCPU != new_cpus:
        # set the new Cpu count
        spec.set_element_numCPUs(new_cpus)

    device_config_specs = []
    if new_hdd:
        disk_size = get_disk_size(vm_obj)
        if new_hdd * 1024 * 1024 > disk_size:
            disk = get_disks(vm_obj)[-1]
            hdd_in_GB = new_hdd * 1024 * 1024
            new_disk_size = hdd_in_GB - disk_size + disk.capacityInKB

            device_config_spec = spec.new_deviceChange()
            device_config_spec.set_element_operation('edit')
            disk._obj.set_element_capacityInKB(new_disk_size)
            device_config_spec.set_element_device(disk._obj)
            device_config_specs.append(device_config_spec)

    if new_iso:
        media_device = get_cd(vm_obj)
        connectable = media_device._obj.new_connectable()
        connectable.set_element_allowGuestControl(False)

        if new_iso.get("name") and new_iso["name"] != "":
            connectable.set_element_connected(True)
            connectable.set_element_startConnected(True)
            media_device._obj.set_element_connectable(connectable)

            backing = VCdIsoBackingInfo()
            backing.set_element_fileName(new_iso["name"])
            media_device._obj.set_element_backing(backing)
        else:
            connectable.set_element_connected(False)
            connectable.set_element_startConnected(False)
            media_device._obj.set_element_connectable(connectable)

        device_config_spec = spec.new_deviceChange()
        device_config_spec.set_element_operation('edit')
        device_config_spec.set_element_device(media_device._obj)

        device_config_specs.append(device_config_spec)

    if len(device_config_specs) != 0:
        spec.set_element_deviceChange(device_config_specs)

    if new_annotation:
        spec.set_element_annotation("\n".join(new_annotation))

    request.set_element_spec(spec)
    ret = server._proxy.ReconfigVM_Task(request)._returnval

    # Wait for the task to finish
    task = VITask(ret, server)
    status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
    if status != task.STATE_SUCCESS:
        raise HypervisorError("Guest:update %s" % task.get_error_message())


def enable_vmi(server, vm_obj):
    request = VI.ReconfigVM_TaskRequestMsg()
    _this = request.new__this(vm_obj._mor)
    _this.set_attribute_type(vm_obj._mor.get_attribute_type())
    request.set_element__this(_this)
    spec = request.new_spec()

    device_config_specs = []

    media_device = VirtualMachineVMIROM()
    media_device.set_element_key(11000)
    device_config_spec = spec.new_deviceChange()
    device_config_spec.set_element_operation('add')
    device_config_spec.set_element_device(media_device)
    device_config_specs.append(device_config_spec)

    spec.set_element_deviceChange(device_config_specs)

    request.set_element_spec(spec)
    ret = server._proxy.ReconfigVM_Task(request)._returnval

    # Wait for the task to finish
    task = VITask(ret, server)
    status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
    if status != task.STATE_SUCCESS:
        raise HypervisorError("Guest:update %s" % task.get_error_message())


def export(server, vm_obj):
    # Request an export
    request = VI.ExportVmRequestMsg()
    _this = request.new__this(vm_obj._mor)
    _this.set_attribute_type(vm_obj._mor.get_attribute_type())
    request.set_element__this(_this)
    ret = server._proxy.ExportVm(request)

    # List of urls to download
    mor = ret._returnval
    http = VIProperty(connection, ret._returnval)
    url = http.info.deviceUrl[0].url

    # TODO: actually download them.

    # Set to 100%
    request = VI.HttpNfcLeaseProgressRequestMsg()
    _this = request.new__this(mor)
    _this.set_attribute_type(MORTypes.HttpNfcLease)
    request.set_element__this(_this)
    request.set_element_percent(100)
    server._proxy.HttpNfcLeaseProgress(request)

    # Completes the request
    request = VI.HttpNfcLeaseCompleteRequestMsg()
    _this = request.new__this(mor)
    _this.set_attribute_type(MORTypes.HttpNfcLease)
    request.set_element__this(_this)
    server._proxy.HttpNfcLeaseComplete(request)


def delete_vm(server, vm_obj):
    # Invoke Destroy_Task
    request = VI.Destroy_TaskRequestMsg()
    _this = request.new__this(vm_obj._mor)
    _this.set_attribute_type(vm_obj._mor.get_attribute_type())
    request.set_element__this(_this)
    ret = server._proxy.Destroy_Task(request)._returnval

    # Wait for the task to finish
    task = VITask(ret, server)

    status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
    if status != task.STATE_SUCCESS:
        raise HypervisorError("Guest:delete %s" % task.get_error_message())


def get_tags(vm_obj):
    return vm_obj.properties.config.annotation.splitlines()


def delete_tag(tag_name, vm_obj):
    tags = get_tags(vm_obj)
    for tag in tags[:]:
        if tag == tag_name:
            tags.remove(tag_name)

    return tags


def create_tag(tag, vm_obj):
    tags = get_tags(vm_obj)
    tags.append(tag)
    return tags


def get_cd(vm_obj):
    for device in vm_obj.properties.config.hardware.device:
        if device._type == "VirtualCdrom":
            return device


def get_disks(vm_obj):
    disks = []
    for device in vm_obj.properties.config.hardware.device:
        if device._type == "VirtualDisk":
            disks.append(device)
    return disks


def get_disk_size(vm_obj):
    size = 0
    for disk in get_disks(vm_obj):
        size += disk.capacityInKB
    return size


def get_network_interfaces(vm_obj):
    vif_types = [
        "VirtualEthernetCard", "VirtualE1000", "VirtualE1000e",
        "VirtualPCNet32", "VirtualVmxnet"
    ]
    vifs = []
    for device in vm_obj.properties.config.hardware.device:
        if device._type in vif_types:
            vifs.append(device)
    return vifs


def create_snapshot(server, vm_obj, snapshot_name):
    snapshot_id = str(uuid.uuid4())
    request = VI.CreateSnapshot_TaskRequestMsg()
    _this = request.new__this(vm_obj._mor)
    _this.set_attribute_type(vm_obj._mor.get_attribute_type())
    request.set_element__this(_this)

    request.set_element_name(snapshot_name)
    request.set_element_description(snapshot_id)
    request.set_element_memory(False)
    request.set_element_quiesce(False)

    ret = server._proxy.CreateSnapshot_Task(request)._returnval
    task = VITask(ret, server)

    status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])

    if status != task.STATE_SUCCESS:
        raise HypervisorError("Snapshot:create %s" % task.get_error_message())

    vm_obj.refresh_snapshot_list()
    return get_snapshot(vm_obj, snapshot_id)


def get_snapshot(vm_obj, snapshot_id):
    regex = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
    if re.match(regex, snapshot_id, re.I):
        for snap in vm_obj.get_snapshots():
            if snap.get_description() == snapshot_id:
                return snap
    else:
        for snap in vm_obj.get_snapshots():
            if snap.get_name() == snapshot_id:
                return snap


def revert_to_snapshot(server, vm_obj, snapshot_obj):
    request = VI.RevertToSnapshot_TaskRequestMsg()
    mor_snap = request.new__this(snapshot_obj._mor)
    mor_snap.set_attribute_type(snapshot_obj._mor.get_attribute_type())
    request.set_element__this(mor_snap)
    ret = server._proxy.RevertToSnapshot_Task(request)._returnval
    task = VITask(ret, server)

    status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
    if status != task.STATE_SUCCESS:
        raise HypervisorError("Snapshot:revert %s" % task.get_error_message())


def delete_snapshot(server, vm_obj, snapshot_obj, remove_children=False):
    request = VI.RemoveSnapshot_TaskRequestMsg()
    mor_snap = request.new__this(snapshot_obj._mor)
    mor_snap.set_attribute_type(snapshot_obj._mor.get_attribute_type())
    request.set_element__this(mor_snap)
    request.set_element_removeChildren(remove_children)
    ret = server._proxy.RemoveSnapshot_Task(request)._returnval
    task = VITask(ret, server)

    status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
    vm_obj.refresh_snapshot_list()
    if status != task.STATE_SUCCESS:
        raise HypervisorError("Snapshot:delete %s" % task.get_error_message())
