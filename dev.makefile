simplestack_cfg = etc/simplestack.cfg
simplestack_env = SIMPLESTACK_CFG=$(simplestack_cfg)

export simplestack_env

bin_pip         = pip
bin_python      = python
bin_console     = python
venv_dir        = .venv
venv_bin        = $(venv_dir)/bin

clean:
	@find . -name '*.pyc' -delete

pep:
	@$(venv_bin)/pep8 --repeat --show-source src setup.py

install_venv:
	$(bin_pip) install virtualenv

create_venv: install_venv
	# Unfortunately libvirt doesn't work inside virtualenv
	virtualenv --system-site-packages $(venv_dir)

bootstrap: create_venv
	$(venv_bin)/$(bin_pip) install -r pip-requires

test:
	@$(simplestack_env) $(venv_bin)/nosetests $(TEST)

env:
	@echo $(simplestack_env)

server:
	$(simplestack_env) bin/simplestack -a foreground -p var/run/simplestack/ -l log/

console:
	PYTHONPATH=src $(simplestack_env) $(bin_console)
