# Simplestack

A simple abstraction layer to deal with different hypervisors.


## Documentation

http://simplestack.rtfd.org


## Development

Simplestack is developed using Python 2.7 and some dependencies described on
the `pip-requires` file available on the project root.

There are some tasks available in the `dev.makefile` file to help bootstraping
Simplestack project for development.

Use `make -f dev.makefile bootstrap` to create a
[virtualenv](http://pypi.python.org/pypi/virtualenv) environment under .venv
directory.

Just read the `dev.makefile` file for more informations on what it does.

### Docker

Just build your container based on our Dockerfile:

    docker build -t simplestack .

And run your container:

    docker run -p 8081:8081 -v $(pwd):/simplestack -it simplestack make -f /simplestack/dev.makefile server


## License

APACHE 2.0
