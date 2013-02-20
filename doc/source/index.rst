===========
Simplestack
===========

Simplestack was made to be the layer between a provisioning application and
many different hypervisors.

The main goal for Simplestack is to connect to different hypervisor and execute
atomic tasks, no logic to handle hosts or complex tasks was added leaving that
responsability to the client application using it.

When executing any command through Simplestack (refer to :doc:`REST API
<restapi>` for more informations) the user (or application) should provide the
hypervisor and host as URL parameters because Simplestack is stateless and just
execute a simple task on a given target.


Virtualization support
======================

Unfortunately not all hypervisors have support to all features the Simplestack
API provides and when the hypervisor could not deal with this operation or
Simplestack doesn't have the implementation for the requested operation it will
raise the (*NotImplementedError*) exception.

The current implementation state for Simplestack can be seen below.

Fully implemented
-----------------

* Xen

Work in progress
----------------

* VMware
* KVM

Future
------

* LXC
* HyperV

**Fully implemented** means it is being used to create and manage virtual
machines on a large infrastructure.


REST API
========

Simplestack provides an HTTP REST interface to run commands on a given
hypervisor. Some informations must be sent for Simplestack to decide on which
hypervisor it needs to connect and the auth keys.

Example:

        http://simplestack.mycompany.com/xen/10.0.0.1/guests

This URL makes Simplestack to connect to a Xen hypervisor that has the address
10.0.0.1 as a master.

The `username` and `password` should be sent as a "token" identified as the
`x-simplestack-hypervisor-token` header. The token is just a simple base64
encoded string of `user:password`.

An example with curl would be:

        curl -H "x-simplestack-hypervisor-token:c2ltcGxlc3RhY2s6c2ltcGxlUDRzNXcwckQ=" http://simplestack.mycompany.com/xen/10.0.0.1/guests

Where `x-simplestack-hypervisor-token` is a base64 encoded string for the user
and password: simplestack:simpleP4s5w0rD.

For more information on the available endpoints for hypervisor operations
please refer to the :doc:`REST API reference <restapi>`.
