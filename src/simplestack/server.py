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
# @author: Juliano Martinez (ncode), Locaweb.

from gevent import monkey
monkey.patch_all()

import os
import grp
import pwd
import json
import time
import base64
import logging

import bottle

from bottle import delete, put, get, post, error, redirect, run, debug
from bottle import abort, request, ServerAdapter, response, static_file
from bottle import error, HTTPError

from simplestack.common.config import config
from simplestack.common.logger import set_logger

app = bottle.app()
LOG = logging.getLogger('simplestack.server')


@error(500)
def custom500(error):
    response.content_type = "application/json"

    traceback = None
    if type(error) is HTTPError:
        traceback = error.traceback
        error = error.exception
    error_class = error.__class__.__name__

    LOG.error("%s: %s", error_class, error)

    return json.dumps({
        "error": error_class,
        "message": str(error),
        "traceback": traceback
    })


@error(404)
def error404(error):
    response.content_type = 'application/json'

    return json.dumps({
        "error": error_class,
        "message": error.output
    })


@get('/:hypervisor/:host')
def pool_info(hypervisor, host):
    """
    Get pool information

    ::

      GET /:hypervisor/:host

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    pool_info = manager.pool_info()

    manager.logout()

    return json.dumps(pool_info)


@get('/:hypervisor/:host/hosts')
def host_list(hypervisor, host):
    """
    Get hosts for a given pool

    ::

      GET /:hypervisor/:host/hosts

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    host_list = manager.host_list()

    manager.logout()

    return json.dumps(host_list)


@get('/:hypervisor/:host/hosts/:host_id')
def host_info(hypervisor, host, host_id):
    """
    Get host info

    ::

      GET /:hypervisor/:host/hosts/:host_id

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    host_info = manager.host_info(host_id)

    manager.logout()

    return json.dumps(host_info)


@get('/:hypervisor/:host/storages')
def storage_list(hypervisor, host):
    """
    Get storages for a given pool

    ::

      GET /:hypervisor/:host/storages

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    storage_list = manager.storage_list()

    manager.logout()

    return json.dumps(storage_list)


@get('/:hypervisor/:host/storages/:storage_id')
def storage_info(hypervisor, host, storage_id):
    """
    Get storage info

    ::

      GET /:hypervisor/:host/storages/:storage_id

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    storage_info = manager.storage_info(storage_id)

    manager.logout()

    return json.dumps(storage_info)


@post('/:hypervisor/:host/storages/:storage_id/guests')
def storage_guest_import(hypervisor, host, storage_id):
    """
    Import a new guest

    ::

      POST /:hypervisor/:host/storages/:storage_id/guests

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    guest = manager.guest_import(
        request.environ['wsgi.input'],
        request.content_length,
        storage_id
    )
    location = "/%s/%s/guests/%s" % (hypervisor, host, guest["id"])
    response.set_header("Location", location)

    manager.logout()

    return json.dumps(guest)


@get('/:hypervisor/:host/guests')
def guest_list(hypervisor, host):
    """
    Get guests for a given pool

    ::

      GET /:hypervisor/:host/guests

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    guest_list = manager.guest_list()

    manager.logout()

    return json.dumps(guest_list)


@post('/:hypervisor/:host/guests')
def guest_create(hypervisor, host):
    """
    Create a new guest

    ::

      POST /:hypervisor/:host/guests

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    data = json.loads(data)
    guest = manager.guest_create(data)
    location = "/%s/%s/guests/%s" % (hypervisor, host, guest["id"])
    response.set_header("Location", location)

    manager.logout()

    return json.dumps(guest)


@post('/:hypervisor/:host/guests')
def guest_import(hypervisor, host):
    """
    Import a new guest

    ::

      POST /:hypervisor/:host/guests

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    guest = manager.guest_import(
        request.environ['wsgi.input'],
        request.content_length
    )
    location = "/%s/%s/guests/%s" % (hypervisor, host, guest["id"])
    response.set_header("Location", location)

    manager.logout()

    return json.dumps(guest)


@get('/:hypervisor/:host/guests/:guest_id')
def guest_info(hypervisor, host, guest_id):
    """
    Get guest informations

    ::

      GET /:hypervisor/:host/guests/:guest_id

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    guest_id = manager.guest_info(guest_id)

    manager.logout()

    return json.dumps(guest_id)


@put('/:hypervisor/:host/guests/:guest_id')
def guest_update(hypervisor, host, guest_id):
    """
    Update guest informations

    ::

      PUT /:hypervisor/:host

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    data = json.loads(data)
    guest_data = manager.guest_update(guest_id, data)

    manager.logout()

    return json.dumps(guest_data)


@post('/:hypervisor/:host/guests/:guest_id/clone')
def guest_clone(hypervisor, host, guest_id):
    """
    Clone a guest

    ::

      POST /:hypervisor/:host/guests/:guest_id/clone

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    data = json.loads(data)
    guest = manager.guest_clone(guest_id, data)
    location = "/%s/%s/guests/%s" % (hypervisor, host, guest["id"])
    response.set_header("Location", location)

    manager.logout()

    return json.dumps(guest)


@get('/:hypervisor/:host/guests/:guest_id/export')
def guest_export(hypervisor, host, guest_id):
    """
    Export guest file

    ::

      GET /:hypervisor/:host/guests/:guest_id/export

    """
    response.content_type = "application/octet-stream"
    manager = create_manager(hypervisor, host)
    export_response, export_length = manager.guest_export(guest_id)
    response_part = export_response.read(1024)
    while response_part:
        yield response_part
        response_part = export_response.read(1024)

    manager.logout()


@delete('/:hypervisor/:host/guests/:guest_id')
def guest_delete(hypervisor, host, guest_id):
    """
    Deletes guest

    ::

      DELETE /:hypervisor/:host/guests/:guest_id

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    guest_delete = manager.guest_delete(guest_id)

    manager.logout()

    return json.dumps(guest_delete)


@get('/:hypervisor/:host/guests/:guest_id/disks')
def disk_list(hypervisor, host, guest_id):
    """
    Get all disks for a given guest

    ::

      GET /:hypervisor/:host/guests/:guest_id/disks

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    disk_list = manager.disk_list(guest_id)

    manager.logout()

    return json.dumps(disk_list)


@post('/:hypervisor/:host/guests/:guest_id/disks')
def disk_create(hypervisor, host, guest_id):
    """
    Create a disk for a given guest

    ::

      POST /:hypervisor/:host/guests/:guest_id/disks

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    data = json.loads(data)
    disk = manager.disk_create(guest_id, data)
    location = "/%s/%s/guests/%s/disks/%s" % (
        hypervisor, host, guest_id, disk["id"]
    )
    response.set_header("Location", location)

    manager.logout()

    return json.dumps(disk)


@get('/:hypervisor/:host/guests/:guest_id/disks/:disk_id')
def disk_info(hypervisor, host, guest_id, disk_id):
    """
    Get a disk in a given guest

    ::

      GET /:hypervisor/:host/guests/:guest_id/disks/:disk_id

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    nwi_info = manager.disk_info(guest_id, disk_id)

    manager.logout()

    return json.dumps(nwi_info)


@put('/:hypervisor/:host/guests/:guest_id/disks/:disk_id')
def disk_update(hypervisor, host, guest_id, disk_id):
    """
    Update a disk in a given guest

    ::

      PUT /:hypervisor/:host/guests/:guest_id/disks/:disk_id

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    data = json.loads(data)
    nwi_info = manager.disk_update(guest_id, disk_id, data)

    manager.logout()

    return json.dumps(nwi_info)


@delete('/:hypervisor/:host/guests/:guest_id/disks/:disk_id')
def disk_delete(hypervisor, host, guest_id, disk_id):
    """
    Delete a disk from a given guest

    ::

      DELETE /:hypervisor/:host/guests/:guest_id/disks/:disk_id

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    manager.disk_delete(guest_id, disk_id)
    manager.logout()


@put('/:hypervisor/:host/guests/:guest_id/media_device')
def media_mount(hypervisor, host, guest_id):
    """
    Mounts an ISO to a CD/DVD drive

    ::

      PUT /:hypervisor/:host/guests/:guest_id/media_device

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    data = json.loads(data)
    manager.media_mount(guest_id, data)
    manager.logout()


@get('/:hypervisor/:host/guests/:guest_id/media_device')
def media_info(hypervisor, host, guest_id):
    """
    Gets the mounted media device name

    ::

      GET /:hypervisor/:host/guests/:guest_id/media_device

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    media_info = manager.media_info(guest_id)

    manager.logout()

    return json.dumps(media_info)


@get('/:hypervisor/:host/networks')
def network_list(hypervisor, host):
    """
    Get networks for a given pool

    ::

      GET /:hypervisor/:host/networks

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    network_list = manager.network_list()

    manager.logout()

    return json.dumps(network_list)


@post('/:hypervisor/:host/networks')
def network_vlan_create(hypervisor, host):
    """
    Create a Network with a tagged VLAN

    ::

      POST /:hypervisor/:host/networks


    The body should contain a JSON object. The required keys should vary for
    each hypervisor.

    Xen example:
    {"name": "VLAN2",
     "description": "VLAN 2 storage",
     "from_network": "BOND1",
     "vlan": 2,
     "other_config": {}}
    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    data = json.loads(data)
    network_ref = manager.network_vlan_create(data["name"], data["description"], data["from_network"], data["vlan"], data["other_config"])
    location = "/%s/%s/networks/%s" % (
        hypervisor, host, network_ref
    )
    response.set_header("Location", location)

    manager.logout()

    return json.dumps(network_ref)


@get('/:hypervisor/:host/networks/:network')
def network_info(hypervisor, host, network):
    """
    Get network info

    ::

      GET /:hypervisor/:host/networks/:network

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    network_info = manager.network_info(network)

    manager.logout()

    return json.dumps(network_info)


@get('/:hypervisor/:host/guests/:guest_id/network_interfaces')
def network_interface_list(hypervisor, host, guest_id):
    """
    Get all network interfaces for a given guest

    ::

      GET /:hypervisor/:host/guests/:guest_id/network_interfaces

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    netiface_list = manager.network_interface_list(guest_id)

    manager.logout()

    return json.dumps(netiface_list)


@post('/:hypervisor/:host/guests/:guest_id/network_interfaces')
def network_interface_create(hypervisor, host, guest_id):
    """
    Create a network interface for a given guest

    ::

      POST /:hypervisor/:host/guests/:guest_id/network_interfaces


    The body should contain a JSON object. The required keys should vary for
    each hypervisor.

    Xen example:
    {"network": "THE NETWORK NAME"}
    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    data = json.loads(data)
    network_interface = manager.network_interface_create(guest_id, data)
    location = "/%s/%s/guests/%s/network_interfaces/%s" % (
        hypervisor, host, guest_id, network_interface["id"]
    )
    response.set_header("Location", location)

    manager.logout()

    return json.dumps(network_interface)


@get('/:hypervisor/:host/guests/:guest_id/network_interfaces/:interface_id')
def network_interface_info(hypervisor, host, guest_id, interface_id):
    """
    Get a network interface in a given guest

    ::

      GET /:hypervisor/:host/guests/:guest_id/network_interfaces/:interface_id

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    nwi_info = manager.network_interface_info(guest_id, interface_id)

    manager.logout()

    return json.dumps(nwi_info)


@put('/:hypervisor/:host/guests/:guest_id/network_interfaces/:interface_id')
def network_interface_update(hypervisor, host, guest_id, interface_id):
    """
    Update a network interface in a given guest

    ::

      PUT /:hypervisor/:host/guests/:guest_id/network_interfaces/:interface_id

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    data = json.loads(data)
    nwi_info = manager.network_interface_update(guest_id, interface_id, data)

    manager.logout()

    return json.dumps(nwi_info)


@delete('/:hypervisor/:host/guests/:guest_id/network_interfaces/:interface_id')
def network_interface_delete(hypervisor, host, guest_id, interface_id):
    """
    Delete a network interface from a given guest

    ::

      DELETE /:hypervisor/:host/guests/:guest_id/network_interfaces/:if_id

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    manager.network_interface_delete(guest_id, interface_id)
    manager.logout()


@get('/:hypervisor/:host/guests/:guest_id/tags')
def tag_list(hypervisor, host, guest_id):
    """
    Get all tags for a given guest

    ::

      GET /:hypervisor/:host/guests/:guest_id/tags

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    tag_list = manager.tag_list(guest_id)

    manager.logout()

    return json.dumps(tag_list)


@post('/:hypervisor/:host/guests/:guest_id/tags')
def tag_create(hypervisor, host, guest_id):
    """
    Create a new tag for a given guest

    ::

      POST /:hypervisor/:host/guests/:guest_id/tags

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    data = json.loads(data)
    tag = manager.tag_create(guest_id, data.get('name'))
    #TODO: Should we return the Location for the first tag?
    location = "/%s/%s/guests/%s/tags/%s" % (
        hypervisor, host, guest_id, tag[0]
    )
    response.set_header("Location", location)

    manager.logout()

    return json.dumps(tag)


@delete('/:hypervisor/:host/guests/:guest_id/tags/:tag_name')
def tag_delete(hypervisor, host, guest_id, tag_name):
    """
    Delete a given tag for a given guest

    ::

      DELETE /:hypervisor/:host/guests/:guest_id/tags

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    tag_delete = manager.tag_delete(guest_id, tag_name)

    manager.logout()

    return json.dumps(tag_delete)


@get('/:hypervisor/:host/guests/:guest_id/snapshots')
def snapshot_list(hypervisor, host, guest_id):
    """
    Get all snapshots for a given guest

    ::

      GET /:hypervisor/:host/guests/:guest_id/snapshots

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    snapshot_list = manager.snapshot_list(guest_id)

    manager.logout()

    return json.dumps(snapshot_list)


@post('/:hypervisor/:host/guests/:guest_id/snapshots')
def snapshot_create(hypervisor, host, guest_id):
    """
    Create a snapshot for a given guest

    ::

      POST /:hypervisor/:host/guests/:guest_id/snapshots

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    data = json.loads(data)
    snapshot = manager.snapshot_create(guest_id, data.get('name'))
    location = "/%s/%s/guests/%s/snapshots/%s" % (
        hypervisor, host, guest_id, snapshot["id"]
    )
    response.set_header("Location", location)

    manager.logout()

    return json.dumps(snapshot)


@get('/:hypervisor/:host/guests/:guest_id/snapshots/:snapshot_id')
def snapshot_info(hypervisor, host, guest_id, snapshot_id):
    """
    Get snapshot informations for a given guest_id and snapshot_id

    ::

      GET /:hypervisor/:host/guests/:guest_id/snapshots/:snapshot_id

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    snapshot_info = manager.snapshot_info(guest_id, snapshot_id)

    manager.logout()

    return json.dumps(snapshot_info)


@put('/:hypervisor/:host/guests/:guest_id/snapshots/:snapshot_id/revert')
def snapshot_revert(hypervisor, host, guest_id, snapshot_id):
    """
    Remove a snapshot for a given guest_id and snapshot_id

    ::

      PUT /:hypervisor/:host/guests/:guest_id/snapshots/:snapshot_id/revert

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    snapshot_revert = manager.snapshot_revert(guest_id, snapshot_id)

    manager.logout()

    return json.dumps(snapshot_revert)


@delete('/:hypervisor/:host/guests/:guest_id/snapshots/:snapshot_id')
def snapshot_delete(hypervisor, host, guest_id, snapshot_id):
    """
    Remove a snapshot for a given guest_id and snapshot_id

    ::

      DELETE /:hypervisor/:host/guests/:guest_id/snapshots/:snapshot_id

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    snapshot_delete = manager.snapshot_delete(guest_id, snapshot_id)

    manager.logout()

    return json.dumps(snapshot_delete)


@put('/:hypervisor/:host/guests/:guest_id/reboot')
def reboot_guest(hypervisor, host, guest_id):
    """
    Reboot a guest based on the given guest_id

    ::

      PUT /:hypervisor/:host/guests/:guest_id/reboot

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)

    data = request.body.readline()
    force = False

    if data:
        data = json.loads(data)
        force = data.get('force')

    manager.guest_reboot(guest_id, force=force)
    manager.logout()

    return json.dumps({"action": "reboot", "message": "ok"})


@put('/:hypervisor/:host/guests/:guest_id/power')
def power_guest(hypervisor, host, guest_id):
    """
    Turn a guest on/off based on a given guest_id

    ::

      PUT /:hypervisor/:host/guests/:guest_id/power

    """
    response.content_type = "application/json"
    manager = create_manager(hypervisor, host)
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    data = json.loads(data)
    state = data['state']
    if state == "force_stop":
        manager.guest_shutdown(guest_id, force=True)
    elif state == "start":
        manager.guest_start(guest_id)
    elif state == "stop":
        manager.guest_shutdown(guest_id, force=False)
    elif state == "pause":
        manager.guest_suspend(guest_id)
    elif state == "resume":
        manager.guest_resume(guest_id)

    manager.logout()

    return json.dumps({"action": state, "message": "ok"})


def parse_token(token):
    decoded_token = base64.b64decode(token).split(':')
    username = decoded_token.pop(0)
    password = ':'.join(decoded_token)
    return (username, password)


def create_manager(hypervisor, host):
    hypervisor_token = request.headers.get("x-simplestack-hypervisor-token")
    if not hypervisor_token:
        abort(401, 'No x-simplestack-hypervisor-token header provided')

    username, password = parse_token(hypervisor_token)

    module = __import__("simplestack.hypervisors.%s" % hypervisor)
    module = getattr(module.hypervisors, hypervisor)

    return module.Stack({
        "api_server": host,
        "username": username,
        "password": password
    })


def main(action):
    if not action == "foreground":
        os.setgid(grp.getgrnam('nogroup')[2])
        os.setuid(pwd.getpwnam(config.get("server", "user"))[2])

    debug(config.getboolean("server", "debug"))
    port = config.getint("server", "port")
    bind_addr = config.get("server", "bind_addr")
    set_logger()
    LOG.info("Starting Simplestack server")
    run(host=bind_addr, port=port, server="gevent")
