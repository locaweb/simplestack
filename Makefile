clean:
	@find . -name '*.pyc' -delete

pep:
	pep8 --exclude=asdf.py --repeat --show-source src setup.py
