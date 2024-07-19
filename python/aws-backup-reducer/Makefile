#!/usr/bin/env make

include ../Makefile

run: override bucket ?=
run: ${python_executable} aws-backup-reducer.py
	@${python_executable} aws-backup-reducer.py
