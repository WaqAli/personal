#! /bin/bash
virtualenv --no-site-packages ./python/gene/env
source ./python/gene/env/bin/activate
pip install --upgrade nose
export PYTHONPATH=$PYTHONPATH:./python/gene
nosetests --with-xunit ./python/gene/test/unit/test_utils.py --xunit-file="/local/system-local/scratch/waqar/zulu/nosetests-unit.xml"

