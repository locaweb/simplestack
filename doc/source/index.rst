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
raise the (**NotImplementedError**) exception.

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


Using
=====

* :doc:`REST API <restapi>`
* :doc:`REST API Endpoints <restapi_autodoc>`
