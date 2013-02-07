===========
Simplestack
===========

Simplestack was made to be the layer between a provisioning application and
many different hypervisors.


Virtualization support
======================

The entry point to work with Simplestack is the HTTP :doc:`REST API <restapi>`.
Each method has the hypervisor and host as the first parameters helping
Simplestack to stay simple handling hypervisor operation and providing the same
API for all operations.

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

* :doc:`REST API reference <restapi>`
