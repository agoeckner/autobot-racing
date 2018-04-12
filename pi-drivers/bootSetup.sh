#!/bin/bash

FILE=/etc/init.d/EthernetInterface

cat > $FILE <<- EOM
#!/bin/sh

### BEGIN INIT INFO
# Provides:          autobot-racing
# Required-Start:    $all
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Starts event loop for autobot racing
# Description:       Creates host connection for autobot-racing and begins taking
#                    messages to send to RC controller
### END INIT INFO

# Author: Ben Huemann <bhuemann@purdue.edu>

DESC="Autobot-racing event loop"
DAEMON=/usr/sbin/EthernetInterface

LOGNAME=$(date +%R_%F)
LOGPATH="/home/pi/autobot-racing/pi-drivers/log/$LOGNAME"
mkdir /home/pi/autobot-racing/pi-drivers/log

#Give some time for DHCP to resolve
sleep 10

python3 /home/pi/autobot-racing/pi-drivers/EthernetInterface.py >> $LOGPATH &
chmod u+rw,g+rw,o+r $LOGPATH
EOM

/etc/init.d/update-rc.d EthernetInterface defaults
