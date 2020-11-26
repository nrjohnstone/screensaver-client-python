#!/bin/sh
### BEGIN INIT INFO
# Provides:             screensaver-start.sh
# Required-Start:       remote_fs $syslog
# Required-Stop:        remote_fs $syslog
# Default-Start:        2 3 4 5
# Default-Stop:         0 1 6
# Short Description:    Start screensaver
# Description:          Start screensaver
### END INIT INFO
sudo python /opt/screensaver-client-python/screensaver.py