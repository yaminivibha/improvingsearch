#!/bin/bash
sudo apt-get -y update
sudo apt-get install python3-pip
sudo apt-get install python3.7
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
sudo -H pip3 install --upgrade pip
sudo pip3 install --upgrade google-api-python-client
sudo apt-get install python-setuptools python-dev build-essential
sudo pip install -r requirements.txt