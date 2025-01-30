#!/usr/bin/env make

include ${shell git rev-parse --show-toplevel}/python/Makefile

run: override bucket ?=
run: ${venv}/bin/python backup-reducer.py
	@${venv}/bin/python backup-reducer.py
