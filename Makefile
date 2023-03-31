all:
	@echo "available targets"
	@echo "- pip-compile: rigenerate requirements.txt"
	@echo "- pip-sync: syncronize virtualenv"
	@echo "- build: build a new package"
	@echo "- clean: remove build generated files"

pip-compile: venv
	.venv/bin/pip-compile --upgrade --annotation-style=line --resolver=backtracking

pip-sync: venv
	.venv/bin/pip-sync --pip-args "install --upgrade pip setuptools" requirements.txt

build: venv
	.venv/bin/python -m build

clean:
	rm -rf dist *.egg-info

venv: .venv

.venv:
	python3.10 -m venv .venv
	.venv/bin/pip install --upgrade pip wheel setuptools
	.venv/bin/pip install -r requirements.txt

.PHONY: all pip-compile pip-sync build clean venv
