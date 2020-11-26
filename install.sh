#!/bin/bash
sudo apt-get install python-pygame -y
sudo apt-get install python-requests -y
sudo apt-get install python-yaml -y

sudo mkdir /opt/screensaver-client-python -p
sudo mkdir /etc/screensaver -p
sudo mkdir /var/log/screensaver -p

sudo rm /opt/screensaver-client-python/*.* -f

sudo cp screensaver.py /opt/screensaver-client-python/
sudo cp PhotoRepository.py /opt/screensaver-client-python/
sudo cp config.template.yml /etc/screensaver/config.yml

sudo sed -i "s|<SCREENSAVER_API_HOST>|$SCREENSAVER_API_HOST|g" /etc/screensaver/config.yml
sudo sed -i "s|<SCREENSAVER_API_PORT>|$SCREENSAVER_API_PORT|g" /etc/screensaver/config.yml
sudo sed -i "s|<SCREEN_SAVER_CLIENT_ID>|$SCREENSAVER_CLIENT_ID|g" /etc/screensaver/config.yml
sudo sed -i "s|<SCREENSAVER_DISPLAY_TIME>|$SCREENSAVER_DISPLAY_TIME|g" /etc/screensaver/config.yml
sudo sed -i "s|<SCREENSAVER_FULL_SCREEN>|$SCREENSAVER_FULL_SCREEN|g" /etc/screensaver/config.yml

# Enable screensaver on boot
sudo cp screensaver-start.sh /etc/init.d/screensaver-start.sh
sudo chmod +x /etc/init.d/screensaver-start.sh
sudo update-rc.d screensaver-start.sh defaults

sudo shutdown -r 1