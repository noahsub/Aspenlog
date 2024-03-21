#!/bin/bash
########################################################################################################################
# linux_run_backend.sh
# This file runs the Aspenlog 2020 backend on a Linux server.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

# Ensure script is not run as sudo
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run as root"
    exit 1
fi

# Kill any existing processes on port 42613
sudo kill $(lsof -t -i:42613) > /dev/null
# Kill any existing screen sessions named 'aspenlog-backend'
screen -S aspenlog-backend -X quit > /dev/null
# Start the backend in a new screen session
screen -dmS aspenlog-backend
screen -S aspenlog-backend -X stuff 'source seeda_python_virtual_environment/bin/activate\n'
screen -S aspenlog-backend -X stuff 'python3.11 main.py\n'