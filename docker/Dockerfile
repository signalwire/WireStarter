#TODO:
# - Install other SDKs 
# - Variablize the space name and API Key
# - Research how to take API key and made Basic Auth Header

FROM debian:buster-slim

ARG NGROK_TOKEN
ARG SIGNALWIRE_SPACE
ARG PROJECT_ID
ARG REST_API_TOKEN
ARG VISUAL

# Install the basic package
RUN apt-get update && apt-get install -y \
    python3     \
    python3-pip \
    apache2     \
    screen      \ 
    jq          \
    curl        \
    less        \
    nano        \
    vim		\
    emacs-nox	

# Install GH Cli
RUN apt-key adv --fetch-keys https://cli.github.com/packages/githubcli-archive-keyring.gpg && echo "deb [arch=$(dpkg --print-architecture)] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list && \
    apt update && apt install gh -y

# Install Ngrok
# TODO eventually may want to change this to not use curl and remove curl from the image.
RUN apt-key adv --fetch-keys https://ngrok-agent.s3.amazonaws.com/ngrok.asc && echo "deb [arch=$(dpkg --print-architecture)] https://ngrok-agent.s3.amazonaws.com buster main" |  tee /etc/apt/sources.list.d/ngrok.list && \
    apt update && apt install ngrok

# Install Python modules 
RUN pip3 install   \
    signalwire     \
    requests       \
    python-dotenv  \
    cmd2           \
    setuptools

# Enable Python -- Apache
# This may need to just be creating the symlink since the image doesn't run
RUN a2enmod cgid

# Configure Ngrok
RUN ngrok config add-authtoken $NGROK_TOKEN

# Copy files to /opt/signalwire
COPY SRC /usr/lib/cgi-bin
COPY SRC/foo_laml.xml.orig /tmp/.foo_laml.xml.orig
RUN chmod +x -R /usr/lib/cgi-bin/

# copy script to start services
COPY start_services.sh /root/start_services.sh
RUN chmod +x /root/start_services.sh

# Pass in VARS #
RUN echo "SIGNALWIRE_SPACE=\"$SIGNALWIRE_SPACE\""  > /usr/lib/cgi-bin/.env
RUN echo "PROJECT_ID=\"$PROJECT_ID\""  >> /usr/lib/cgi-bin/.env
RUN echo "REST_API_TOKEN=\"$REST_API_TOKEN\"" >> /usr/lib/cgi-bin/.env
RUN echo "VISUAL=\"$VISUAL\"" >> /usr/lib/cgi-bin/.env
# Start the user in swsh
RUN echo "python3 /usr/lib/cgi-bin/swsh.py" >> /root/.bashrc
RUN ln -s /usr/lib/cgi-bin/swsh.py /usr/bin/swsh

# Start Apache and ngrok on container start
ENTRYPOINT sed -i -e 's/\r$//' /root/start_services.sh && /root/start_services.sh && /bin/bash
