#!/bin/bash

sudo mkdir /opt/screensaver-client-python

sudo rm /opt/screensaver-client-python/*.* -f

sudo cp screensaver.py /opt/screensaver-client-python/
#sudo cp screensaver.service /lib/systemd/system/
#sudo chmod 644 /lib/systemd/system/screensaver.service

#sudo systemctl daemon-reload
#sudo systemctl enable screensaver.service
#sudo shutdown -r 60