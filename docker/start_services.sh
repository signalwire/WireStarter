#!/bin/bash

# Enable and Start Apache
/usr/sbin/apache2ctl start > /dev/null 2>&1
#apache2ctl -D FOREGROUND

# Start Nrok in a screen
/usr/bin/screen -dmS ngrok /usr/local/bin/ngrok --log=/root/ngrok.log http 9080
sleep 3  # wait for the tunnel to start #

## What is the NGROK URL?
# t=2022-08-26T15:25:29+0000 lvl=info msg="started tunnel" obj=tunnels name=command_line addr=http://localhost:80 url=https://f4ce-24-239-215-106.ngrok.io
NGROK_URL=$( grep url /root/ngrok.log | cut -d= -f 8 | sed 's/https:\/\///g' | tail -1 )
echo $NGROK_URL > /root/ngrok_url

# Run python script to update the numbers
# Pass in ngrok_url as an arg
if [ ! -z $NGROK_URL ]; then
  python3 /usr/lib/cgi-bin/update_laml_bins.py $NGROK_URL
fi

#LocalToNet                                                                                                                                                                                                                                                                                        
if [ ! -z $LOCALTONET_AUTH_TOKEN ]; then
    /usr/bin/screen -dmS localtonet /usr/bin/localtonet authtoken $LOCALTONET_AUTH_TOKEN
    sleep 3
    if [ ! -z $LOCALTONET_API_TOKEN ]; then
	curl -s -o -  -X GET https://localtonet.com/api/GetTunnelsByAuthToken/$LOCALTONET_AUTH_TOKEN -H 'accept: */*' -H "Authorization: Bearer $LOCALTONET_API_TOKEN"| jq -r '.result[].url' | sed 's/https:\/\///g' > /root/localtonet.url
    fi
fi
