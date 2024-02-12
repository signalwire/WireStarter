#!/bin/bash

# Start Ngrok in a screen
if [ ! -z $NGROK_TOKEN ]; then
    /usr/local/bin/ngrok config add-authtoken $NGROK_TOKEN > /dev/null 2>&1
    /usr/bin/screen -dmS ngrok /usr/local/bin/ngrok http $NGROK_ARGS 9080
fi

sleep 3
export HOSTNAME=`curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url' | sed 's/https:\/\///'`

if [ -f "/workdir/.env" ]; then
    cat "/workdir/.env"  | grep . | sed 's/\=/ /' | awk '{print "SetEnv " $0}' >> /etc/apache2/apache2.conf
fi

# Loop so we can update the urls if they change while running.
while true
do
    if [ ! -z $NGROK_TOKEN ]; then
	export NGROK_URL=$( curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url' )
	if [ ! -z $NGROK_URL ]; then
	    # update the numbers that were previously mapped to an ngrok URL previously.
	    python3 /usr/lib/cgi-bin/update_laml_bins.py $NGROK_URL
	fi
    fi

    clear
    echo -e "\n\n";
    cat /.sw.ans
    echo -e "\n\n";
    echo -e "Welcome to WireStarter!";
    echo -e "\n"

    if [ ! -z $NGROK_URL ]; then
	echo -e "NGROK Tunnel: $NGROK_URL";
	echo -e "/workdir/public -> $NGROK_URL/public\n";
    fi
    if [ ! -z $WORKDIR ]; then
	echo -e "Persistent host directory is /workdir -> $WORKDIR\n";
    fi
    
    echo -e "\n-- Thank you!\nsupport@signalwire.com\n\n";
    
    sleep 300
done
