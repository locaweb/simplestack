===========
Simplestack
===========

A simple abstraction layer to deal with different hypervisors.


Virtualization support
======================

The :doc:`REST API <restapi>` uses a given hypervisor and routes
to the respective class to perform the action for that resource.

When the hypervisor doesn't support a specific feature an error
(*NotImplementedError*) will be raised.

The current implementation state for Simplestack can be seen below.


Fully implemented
-----------------

* Xen

Work in progress
----------------

* VMware
* HyperV
* KVM

Future
------

* LXC


REST API
========

* :doc:`REST API reference <restapi>`
