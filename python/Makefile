#!/usr/bin/env make

override python_version ?= 3.12
override python_executable ?= ${shell which 'python${python_version}'}

override venv ?= .venv

create-venv: ${python_executable}
	@${python_executable} -m 'venv' '${venv}'
	@${venv}/bin/pip --require-virtualenv install -U -r 'requirements.txt'

recreate-venv:
	@rm -r '${venv}'
	@${MAKE} create-venv

update-venv: ${venv}/bin/pip
	@${venv}/bin/pip freeze -l --require-virtualenv | sed 's/==/>=/' \
	| xargs ${venv}/bin/pip --require-virtualenv install -U
