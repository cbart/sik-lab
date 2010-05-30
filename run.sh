#!/bin/bash

python ./sklab/run.py $1 &
python ./sklab/server/run.py $1 &
