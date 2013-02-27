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
# @author: Francisco Freire, Locaweb.
# @author: Thiago Morello (morellon), Locaweb.
# @author: Willian Molinari (PotHix), Locaweb.

import os
import libvirt
import xml.etree.ElementTree as et

from simplestack.common.config import config
from simplestack.exceptions import FeatureNotImplemented, EntityNotFound
from simplestack.presenters.formatter import Formatter
from simplestack.decorators.libvirt import *


class SimpleStack(object):
    """
    This module is the base implementation for all hypervisors available.

    It uses libvirt as the fallback implementation and throw an error
    (FeatureNotImplemented) if the hypervisor doesn't have an implementation
    for the given method and doesn't support libvirt also.
    """

    def __init__(self):
        self.connection = False
        self.format_for = Formatter()

    def libvirt_connect(self):
        return libvirt.open(self.libvirt_connection_path())

    def libvirt_connection_path(self):
        proto = config.get("libvirt", "transport")

        if proto == "ssh":
            keyfile = config.get("libvirt", "ssh_keyfile")

            if os.path.exists(keyfile):
                params = "keyfile=%s" % keyfile
            else:
                raise SSHKeyInvalid
        else:
            params = "no_verify=1"

        conn_str = "qemu+%(proto)s://%(username)s@%(server)s/system?%(params)s"

        return(conn_str % {
            "params": params,
            "proto" : proto,
            "server": self.poolinfo.get("api_server"),
            "username": self.poolinfo.get("username"),
        })

    def connect(self):
        """
        Each hypervisor should implement this method to return its own connection
        object or just use the libvirt_connect() here.
        """
        raise FeatureNotImplemented()

    @require_libvirt(True)
    def pool_info(self):
        free = self.libvirt_connection.getFreeMemory()/1024/1024
        total = self.libvirt_connection.getInfo()[1]
        address = self.poolinfo.get("api_server").split(":")[0]

        return self.format_for.pool(total - free, free, address)

    def host_list(self):
        raise FeatureNotImplemented()

    def host_info(self, host_id):
        raise FeatureNotImplemented()

    def storage_list(self):
        raise FeatureNotImplemented()

    def storage_info(self, storage_id):
        raise FeatureNotImplemented()

    @require_libvirt(True)
    def guest_list(self):
        not_running = [
            self.libvirt_vm_info(self.libvirt_connection.lookupByName(vm_name))
            for vm_name in self.libvirt_connection.listDefinedDomains()
        ]
        running = [
            self.libvirt_vm_info(self.libvirt_connection.lookupByID(vm_id))
            for vm_id in self.libvirt_connection.listDomainsID()
        ]
        return not_running + running

    def guest_create(self, guestdata):
        raise FeatureNotImplemented()

    def guest_clone(self, guest_id, guestdata):
        raise FeatureNotImplemented()

    def guest_import(self, gueststream, guestsize, storage_id=None):
        raise FeatureNotImplemented()

    def guest_export(self, guest_id):
        raise FeatureNotImplemented()

    @require_libvirt(True)
    def guest_info(self, guest_id):
        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        return self.libvirt_vm_info(dom)

    @require_libvirt(True)
    def guest_shutdown(self, guest_id, force=False):
        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        if force:
            return dom.destroy()
        else:
            return dom.shutdown()

    @require_libvirt(True)
    def guest_start(self, guest_id):
        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        dom.create()

    @require_libvirt(True)
    def guest_suspend(self, guest_id):
        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        return dom.suspend()

    @require_libvirt(True)
    def guest_resume(self, guest_id):
        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        return dom.resume()

    @require_libvirt(True)
    def guest_reboot(self, guest_id, force=False):
        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        if force:
            return vm.reset(0)
        else:
            return vm.reboot(0)

    def guest_update(self, guest_id, guestdata):
        raise FeatureNotImplemented()

    @require_libvirt(True)
    def guest_delete(self, guest_id):
        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        dom.undefine()
        dom.destroy()

    def disk_list(self, guest_id):
        raise FeatureNotImplemented()

    def disk_create(self, guest_id, data):
        raise FeatureNotImplemented()

    def disk_info(self, guest_id, disk_id):
        raise FeatureNotImplemented()

    def disk_update(self, guest_id, disk_id, data):
        raise FeatureNotImplemented()

    def disk_delete(self, guest_id, disk_id):
        raise FeatureNotImplemented()

    def media_mount(self, guest_id, media_data):
        raise FeatureNotImplemented()

    def media_info(self, guest_id):
        raise FeatureNotImplemented()

    def media_unmount(self, guest_id):
        raise FeatureNotImplemented()

    @require_libvirt(True)
    def network_interface_list(self, guest_id):
        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        root = et.fromstring(dom.XMLDesc(0))

        interfaces = []

        for iface in root.iter("interface"):
            iface_param = {}
            for i in iface.getchildren():
                key = i.attrib.keys()[0]
                iface_param[key] = i.attrib[key]

            # Keeping the contract for id values
            iface_param["id"] = iface_param["address"]
            interfaces.append(iface_param)

        return interfaces

    def network_interface_create(self, guest_id, data):
        raise FeatureNotImplemented()

    @require_libvirt(True)
    def network_interface_info(self, guest_id, network_interface_id):
        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        root = et.fromstring(dom.XMLDesc(0))

        nw_interfaces = self.network_interface_list(guest_id)

        for iface in nw_interfaces:
            if iface["id"] == network_interface_id:
                return iface

        raise EntityNotFound("Network interface", network_interface_id)

    def network_interface_update(self, guest_id, network_interface_id, data):
        raise FeatureNotImplemented()

    def network_interface_delete(self, guest_id, network_interface_id):
        raise FeatureNotImplemented()

    @require_libvirt(True)
    def snapshot_list(self, guest_id):
        dom = self.libvirt_connection.lookupByID(guest_id)
        snaps = [
            self.libvirt_snapshot_info(s)
            for s in dom.snapshotListNames()
        ]
        return snaps

    def snapshot_create(self, guestname, name=None):
        raise FeatureNotImplemented()

    @require_libvirt(True)
    def snapshot_info(self, guestname, snapshot_name):
        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        snap = self.libvirt_get_snapshot(dom, snapshot_id)
        if snap:
            return self.libvirt_snapshot_info(snap)
        else:
            raise EntityNotFound("Snapshot", snapshot_id)

    @require_libvirt(True)
    def snapshot_delete(self, guest_id, snapshot_id):
        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        snap = self.libvirt_get_snapshot(dom, snapshot_id)
        snap.delete(0)

    @require_libvirt(True)
    def snapshot_revert(self, guest_id, snapshot_id):
        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        snap = self.libvirt_get_snapshot(dom, snapshot_id)
        dom.revertToSnapshot(snap)

    def tag_list(self, guest_id):
        raise FeatureNotImplemented()

    def tag_create(self, guest_id, tag_name):
        raise FeatureNotImplemented()

    def tag_delete(self, guest_id, tag_name):
        raise FeatureNotImplemented()

    def libvirt_vm_info(self, dom):
        infos = dom.info()
        return (
            self.format_for.guest(
                dom.UUIDString(),
                dom.name(),
                infos[3],
                infos[1] / 1024,
                None,
                None,
                None,
                None,
                self.state_translation[infos[0]],
                None
            )
        )

    def libvirt_snapshot_info(self, snapshot):
        return (
            self.format_for.snapshot(
                snapshot.get_description(),
                snapshot.name(),
                snapshot.get_state(),
                snapshot.get_path(),
                snapshot.get_create_time()
            )
        )

    def libvirt_get_snapshot(self, dom, snapshot_id):
        pass
