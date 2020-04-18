#!/bin/bash

sudo mkdir /opt/screensaver-client-python

sudo rm /opt/screensaver-client-python/*.* -f

sudo cp screensaver.py /opt/screensaver-client-python/
sudo cp config.template.yml /etc/screensaver/config.yml

sudo sed -i "s|<SCREENSAVER_API_HOST>|$SCREENSAVER_API_HOST|g" /etc/screensaver/config.yml
sudo sed -i "s|<SCREENSAVER_API_PORT>|$SCREENSAVER_API_PORT|g" /etc/screensaver/config.yml
sudo sed -i "s|<SCREEN_SAVER_CLIENT_ID>|SCREEN_SAVER_CLIENT_ID|g" /etc/screensaver/config.yml
sudo sed -i "s|<SCREENSAVER_DISPLAY_TIME>|SCREENSAVER_DISPLAY_TIME|g" /etc/screensaver/config.yml
sudo sed -i "s|<SCREENSAVER_FULL_SCREEN>|SCREENSAVER_FULL_SCREEN|g" /etc/screensaver/config.yml

#sudo cp screensaver.service /lib/systemd/system/
#sudo chmod 644 /lib/systemd/system/screensaver.service

#sudo systemctl daemon-reload
#sudo systemctl enable screensaver.service
#sudo shutdown -r 60