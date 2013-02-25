========
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
please refer to the :doc:`REST API reference <restapi_autodoc>`.
