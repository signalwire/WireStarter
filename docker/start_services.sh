#!/bin/bash

# Enable and Start Apache
/usr/sbin/apache2ctl start > /dev/null 2>&1

# Start Ngrok in a screen
if [ ! -z $NGROK_TOKEN ]; then
    /usr/local/bin/ngrok config add-authtoken $NGROK_TOKEN > /dev/null 2>&1
    /usr/bin/screen -dmS ngrok /usr/local/bin/ngrok --log=/var/log/ngrok.log http 9080
fi

# Start LocalToNet in screen
if [ ! -z $LOCALTONET_AUTH_TOKEN ]; then
    /usr/bin/screen -dmS localtonet /usr/bin/localtonet authtoken $LOCALTONET_AUTH_TOKEN
fi

sleep 2

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
    if [ ! -z $LOCALTONET_API_TOKEN ]; then
	export LOCALTONET_URL=$( curl -s -o -  -X GET https://localtonet.com/api/GetTunnelsByAuthToken/$LOCALTONET_AUTH_TOKEN -H 'accept: */*' -H "Authorization: Bearer $LOCALTONET_API_TOKEN" | jq -r '.result[].url' | head -1 )
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
    if [ ! -z $LOCALTONET_URL ]; then
	echo "LocalToNet Tunnel: $LOCALTONET_URL";
	echo -e "/workdir/public -> $LOCALTONET_URL/public\n";
    fi
    if [ ! -z $WORKDIR ]; then
	echo -e "Persistent host directory is /workdir -> $WORKDIR\n";
    fi
    
    echo -e "\n-- Thank you!\nsupport@signalwire.com\n\n";
    
    sleep 300
done
