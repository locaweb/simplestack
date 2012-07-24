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

from simplestack.exceptions import EntityNotFound
from simplestack.hypervisors.base import SimpleStack
from simplestack.views.format_view import FormatView

import uuid
import random
import datetime


class Stack(SimpleStack):

    defaultdata = {
        "host": "localhost"
        "state": "STARTED",
        "cpus": "4",
        "memory": "1024",
        "snapshots": {},
        "tags": [],
        "tools_up_to_date": False,
        "cd": None,
        "network_interfaces": {
            "00:11:22:33:44:55": {
                "id": "00:11:22:33:44:55",
                "number": "0",
                "mac": "00:11:22:33:44:55",
                "network": "network1"
            }
        }
    }

    guests = {}

    def __init__(self, poolinfo):
        self.connection = False
        self.poolinfo = poolinfo
        self.format_for = FormatView()

    def connect(self):
        pass

    def pool_info(self):
        return self.format_for.pool(1024, 64, "127.0.0.1")

    def guest_list(self):
        return self.guests.values()

    def guest_info(self, guest_id):
        return self.guests.get(guest_id)

    def guest_shutdown(self, guest_id, force=False):
        if not self.guests.get(guest_id):
            raise EntityNotFound("Guest", guest_id)
        self.guests[guest_id]['state'] = "STOPPED"

    def guest_start(self, guest_id):
        if not self.guests.get(guest_id):
            raise EntityNotFound("Guest", guest_id)
        self.guests[guest_id]['state'] = "STARTED"

    def guest_reboot(self, guest_id, force=False):
        pass

    def guest_suspend(self, guest_id):
        if not self.guests.get(guest_id):
            raise EntityNotFound("Guest", guest_id)
        self.guests[guest_id]['state'] = "PAUSED"

    def guest_resume(self, guest_id):
        if not self.guests.get(guest_id):
            raise EntityNotFound("Guest", guest_id)
        self.guests[guest_id]['state'] = "STARTED"

    def guest_create(self, guestdata):
        guest = self.defaultdata.copy()
        guest["id"] = str(uuid.uuid4())
        self.guests[guest["id"]] = guest
        return guest

    def guest_delete(self, guest_id):
        if not self.guests.get(guest_id):
            raise EntityNotFound("Guest", guest_id)
        del self.guests[guest_id]

    def guest_update(self, guest_id, guestdata):
        if not self.guests.get(guest_id):
            raise EntityNotFound("Guest", guest_id)

        self.guests[guest_id].update(guestdata)

        return self.guests[guest_id]

    def media_mount(self, guest_id, media_data):
        if not self.guests.get(guest_id):
            raise EntityNotFound("Guest", guest_id)

        self.guests[guest_id]["cd"] = media_data.get("name")

    def media_info(self, guest_id):
        if not self.guests.get(guest_id):
            raise EntityNotFound("Guest", guest_id)
        return {"name": self.guests[guest_id]["cd"]}

    def network_interface_list(self, guest_id):
        if not self.guests.get(guest_id):
            raise EntityNotFound("Guest", guest_id)

        return self.guests[guest_id]['network_interfaces'].values()

    def network_interface_create(self, guest_id, data):
        if not self.guests.get(guest_id):
            raise EntityNotFound("Guest", guest_id)
        mac = "%02x:%02x:%02x:%02x:%02x:%02x:%02x:%02x" % (
            random.randint(0, 255), random.randint(0, 255),
            random.randint(0, 255), random.randint(0, 255),
            random.randint(0, 255), random.randint(0, 255),
            random.randint(0, 255), random.randint(0, 255)
        )
        self.guests[guest_id]['network_interfaces'][mac] = {
            "id": mac,
            "number": "0",
            "mac": mac,
            "network": "network1"
        }

        return self.guests[guest_id]['network_interfaces'][mac]

    def network_interface_info(self, guest_id, interface_id):
        if not self.guests.get(guest_id):
            raise EntityNotFound("Guest", guest_id)

        return self.guests[guest_id]['network_interfaces'][interface_id]

    def network_interface_update(self, guest_id, interface_id, data):
        if not self.guests.get(guest_id):
            raise EntityNotFound("Guest", guest_id)

        nw_int = self.guests[guest_id]['network_interfaces'][interface_id]
        if data.get("network"):
            nw_int["network"] = data["network"]
        return nw_int

    def network_interface_delete(self, guest_id, interface_id):
        del self.guests[guest_id]['network_interfaces'][interface_id]

    def snapshot_list(self, guest_id):
        return self.guests[guest_id]['snapshots'].values()

    def snapshot_create(self, guest_id, name=None):
        if not name:
            name = str(datetime.datetime.now())
        snapshot_id = str(uuid.uuid4())

        snapshot = {
            'id': snapshot_id,
            'name': name,
            'created': str(datetime.datetime.now())
        }

        self.guests[guest_id]['snapshots'][snapshot_id] = snapshot
        return snapshot

    def snapshot_info(self, guest_id, snapshot_id):
        return self.guests[guest_id]['snapshots'][snapshot_id]

    def snapshot_revert(self, guest_id, snapshot_id):
        pass

    def snapshot_delete(self, guest_id, snapshot_id):
        del self.guests[guest_id]['snapshots'][snapshot_id]

    def tag_list(self, guest_id):
        return self.guests[guest_id]['tags']

    def tag_create(self, guest_id, tag_name):
        self.guests[guest_id]['tags'].append(tag_name)
        return self.guests[guest_id]['tags']

    def tag_delete(self, guest_id, tag_name):
        for tag in self.guests[guest_id]['tags'][:]:
            if tag == tag_name:
                self.guests[guest_id]['tags'].remove(tag_name)

        return self.guests[guest_id]['tags']
