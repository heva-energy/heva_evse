.PHONY: build clean

build: clean
	python3 setup.py sdist bdist_wheel

push:
	twine upload dist/*

install:
	python3 setup.py install


clean:
	rm -rf dist build