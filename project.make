simplestack_cfg = etc/simplestack.cfg
simplestack_env = SIMPLESTACK_CFG=$(simplestack_cfg)

bin_pip         = pip
bin_python      = python
venv_dir        = .venv

clean:
	@find . -name '*.pyc' -delete

pep:
	pep8 --exclude=asdf.py --repeat --show-source src setup.py

install_venv:
	$(bin_pip) install virtualenv

create_venv: install_venv
	virtualenv $(venv_dir)

bootstrap: create_venv
	$(venv_dir)/bin/$(bin_pip) install -r pip-requires

test:
	@$(venv_dir)/bin/nosetests

env:
	@echo $(simplestack_env)
