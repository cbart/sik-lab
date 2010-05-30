#!/bin/bash

MODULES=`find . -iname '*unittests.py'`

for module in $MODULES; do
    echo ""
    echo ""
    echo "TEST: " $module
    python $module -v;
done;
