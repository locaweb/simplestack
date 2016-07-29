simplestack_cfg = etc/simplestack.cfg
simplestack_env = PYTHONPATH=src:$(CURDIR)/vendor/lib/python SIMPLESTACK_CFG=$(simplestack_cfg)

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

# Unfortunately libvirt doesn't work inside virtualenv
create_venv: install_venv
	virtualenv --system-site-packages $(venv_dir)

bootstrap_venv: create_venv
	$(venv_bin)/$(bin_pip) install -r requirements.txt
	$(venv_bin)/$(bin_pip) install -r test-requirements.txt

bootstrap:
	$(bin_pip) install -r requirements.txt
	$(bin_pip) install -r test-requirements.txt

test:
	@$(simplestack_env) $(venv_bin)/nosetests $(TEST)

env:
	@echo $(simplestack_env)

server:
	$(simplestack_env) bin/simplestack -a foreground - p var/run/simplestack/ -l log/

vendor:
	$(bin_pip) install --install-option="--home=$(CURDIR)/vendor" -r requirements.txt

console:
	$(simplestack_env) $(bin_console)
