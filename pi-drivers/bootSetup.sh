#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

cd /etc/init.d
FILE=./EthernetInterface

cat > $FILE <<- EOM
#!/bin/sh

### BEGIN INIT INFO
# Provides:          autobot-racing
# Required-Start:    \$all
# Required-Stop:     \$remote_fs \$syslog
# Default-Start:     3 4 5
# Default-Stop:      0 1 6
# Short-Description: Starts event loop for autobot racing
# Description:       Creates host connection for autobot-racing and begins taking
#                    messages to send to RC controller
### END INIT INFO

# Author: Ben Huemann <bhuemann@purdue.edu>

DESC="Autobot-racing event loop"
DAEMON=/usr/sbin/EthernetInterface

LOGNAME=\$(date +%F)
LOGPATH="/home/pi/autobot-racing/pi-drivers/log/\$LOGNAME"
mkdir /home/pi/autobot-racing/pi-drivers/log

#Give some time for DHCP to resolve
sleep 10

echo "===============================\$(date +%r)================================" >> \$LOGPATH 
python3 /home/pi/autobot-racing/pi-drivers/EthernetInterface.py >> \$LOGPATH &
chmod u+rw,g+rw,o+r \$LOGPATH
EOM

chmod +x EthernetInterface
update-rc.d EthernetInterface defaults > /dev/null
cd - > /dev/null
