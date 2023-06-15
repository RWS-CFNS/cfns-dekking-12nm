#!/bin/bash
# A sample Bash script to execute the python scripts
# Make this run as a service to automatically execute the python programs
export PYTHONPATH=$PYTHONPATH:/usr/lib/python3/dist-packages
#check filenames, because these do not exist. This script will not work.
sudo python3 ./gillMaximetDataSampler_V1.py
sudo python3 ./sshcon.py
