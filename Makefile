#!/bin/bash
help:
	@echo "make"
	@echo "    pypi"
	@echo "        make and upload python package."
pypi:
	rm dist/*.tar.gz
	python setup.py sdist bdist_wheel
	twine upload dist/*.tar.gz