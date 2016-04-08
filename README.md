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

    docker-compose up -d

    docker-compose down

Runing tests:

    docker-compose run web make -f dev.makefile test


## License

APACHE 2.0
