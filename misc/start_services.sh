#!/bin/bash

/etc/init.d/redis-server start > /dev/null 2>&1
/etc/init.d/nginx start > /dev/null 2>&1

# Loop so we can update the urls if they change while running.
while true
do
    clear
    echo -e "\n\n";
    cat /.sw.ans
    echo -e "\n\n";
    echo -e "Welcome to WireStarter!";
    echo -e "\n"

    if [ ! -z $WORKDIR ]; then
	    echo -e "Persistent host directory is /workdir -> $WORKDIR\n";
    fi
    
    echo -e "\n-- Thank you!\nsupport@signalwire.com\n\n";
    
    sleep 300
done
