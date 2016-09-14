#!/usr/bin/env bash

virtualenv --no-site-packages env
source "$( dirname "${BASH_SOURCE[0]}" )/env/bin/activate"
pip install nose

