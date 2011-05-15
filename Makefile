PYTHONPATH=/tmp/pyinstall

env :
	export PYTHONPATH=$(PYTHONPATH)
	-mkdir $(PYTHONPATH)
	python setup.py develop --install-dir=$(PYTHONPATH)

test :
	python -m unittest tests/*py tests/plugins/*/*py

tests : test

.SILENT:
