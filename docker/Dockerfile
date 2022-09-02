#TODO:
# - Install other SDKs 
# - Variablize the space name and API Key
# - Research how to take API key and made Basic Auth Header

FROM debian:buster-slim

ARG NGROK_TOKEN
ARG SIGNALWIRE_SPACE
ARG PROJECT_ID
ARG REST_API_TOKEN

# Install the basic package
RUN apt-get update && apt-get install -y \
    python3     \
    python3-pip \
    apache2     \
    screen      \ 
    curl

# Install Ngrok
# TODO eventually may want to change this to not use curl and remove curl from the image.
RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" |  tee /etc/apt/sources.list.d/ngrok.list && apt update && apt install ngrok

# Install Python modules 
RUN pip3 install   \
    signalwire     \
    requests       \
    python-dotenv  \
    setuptools

# Enable Python -- Apache
# This may need to just be creating the symlink since the image doesn't run
RUN a2enmod cgid

# Configure Ngrok
RUN ngrok config add-authtoken $NGROK_TOKEN

# Copy files to /opt/signalwire
COPY SRC /usr/lib/cgi-bin
RUN chmod +x -R /usr/lib/cgi-bin/

# copy script to start services
COPY start_services.sh /root/start_services.sh
RUN chmod +x /root/start_services.sh

# Pass in VARS #
RUN echo "SIGNALWIRE_SPACE=\"$SIGNALWIRE_SPACE\""  > /usr/lib/cgi-bin/.env
RUN echo "PROJECT_ID=\"$PROJECT_ID\""  >> /usr/lib/cgi-bin/.env
RUN echo "REST_API_TOKEN=\"$REST_API_TOKEN\"" >> /usr/lib/cgi-bin/.env

# Start Apache and ngrok on container start
ENTRYPOINT /root/start_services.sh && /bin/bash
