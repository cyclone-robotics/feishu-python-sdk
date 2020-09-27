help:
	@echo "make"
	@echo "    dist"
	@echo "        make and upload python package."

dist:
	rm -f ./dist/*.tar.gz
	python setup.py sdist bdist_wheel
	twine upload dist/*.tar.gz
