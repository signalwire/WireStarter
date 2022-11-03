#!/bin/bash

# Enable and Start Apache
/usr/sbin/apache2ctl start > /dev/null 2>&1
#apache2ctl -D FOREGROUND

# Start Ngrok in a screen
if [ ! -z $NGROK_TOKEN ]; then
    /usr/local/bin/ngrok config add-authtoken $NGROK_TOKEN
    /usr/bin/screen -dmS ngrok /usr/local/bin/ngrok --log=/root/ngrok.log http 9080
    sleep 3  # wait for the tunnel to start #
    NGROK_URL=$( grep url /root/ngrok.log | cut -d= -f 8 | sed 's/https:\/\///g' | tail -1 )
    echo $NGROK_URL > /root/ngrok.url
    # Run python script to update the numbers
    # Pass in ngrok_url as an arg
    if [ ! -z $NGROK_URL ]; then
	python3 /usr/lib/cgi-bin/update_laml_bins.py $NGROK_URL
    fi
fi

# Start LocalToNet in screen
if [ ! -z $LOCALTONET_AUTH_TOKEN ]; then
    /usr/bin/screen -dmS localtonet /usr/bin/localtonet authtoken $LOCALTONET_AUTH_TOKEN
    sleep 3
    if [ ! -z $LOCALTONET_API_TOKEN ]; then
	curl -s -o -  -X GET https://localtonet.com/api/GetTunnelsByAuthToken/$LOCALTONET_AUTH_TOKEN -H 'accept: */*' -H "Authorization: Bearer $LOCALTONET_API_TOKEN" | jq -r '.result[].url' | \
	    sed 's/https:\/\///g' | head -1 > /root/localtonet.url
    fi
fi

export NGROK_URL=`cat /root/ngrok.url`;
export LOCALTONET_URL=`cat /root/localtonet.url`;

clear
echo -e "\n\n";
cat /.sw.ans
echo -e "\n\n";
echo -e "Welcome to WireStarter!";
echo -e "\n"

if [ ! -z $NGROK_URL ]; then
    echo -e "NGROK Tunnel: https://$NGROK_URL";
    echo -e "/workdir/public -> https://$NGROK_URL/public\n";
fi
if [ ! -z $LOCALTONET_URL ]; then
    echo "LocalToNet Tunnel: https://$LOCALTONET_URL";
    echo -e "/workdir/public -> https://$LOCALTONET_URL/public\n";
fi
if [ ! -z $WORKDIR ]; then
    echo -e "Persistent host directory is /workdir -> $WORKDIR\n";
fi

echo -e "\n-- Thank you!\nsupport@signalwire.com\n\n";

sleep infinity
