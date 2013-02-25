=======================
Simplestack and libvirt
=======================

Simplestack works good with Libvirt but some configurations are required.

Libvirt supports `many different transport protocols
<http://libvirt.org/remote.html>`_ and Simplestack is capable of using any of
them with some customization but was tested just with SSH and TCP.

To use Simplestack for test purposes or locally we recommend to use TCP for the
sake of simplicity, but we (`and libvirt
<http://libvirt.org/remote.html#Remote_transports>`_) **DO NOT** recommend using
it on your production environment.

By default Simplestack uses SSH to connect to libvirtd by using a sample SSH
key (for test purposes) that should be changed for your real SSH key. Your
server needs to be accessible on port 22 using the key specified on
simplestack.cfg file.
