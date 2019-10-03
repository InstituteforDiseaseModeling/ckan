#!/bin/bash
TMPDIR="$(mktemp --directory)" 
trap 'rm -r "${TMPDIR}"' EXIT 
virtualenv -p /usr/bin/python "${TMPDIR}"
source "${TMPDIR}/bin/activate"
python --version
pip install ckanapi
pip install unittest-xml-reporting
python ops_tests.py
