#TODO:
# - Install other SDKs 
# - Variablize the space name and API Key
# - Research how to take API key and made Basic Auth Header

FROM debian:buster-slim

ARG NGROK_TOKEN
ENV NGROK_TOKEN=${NGROK_TOKEN}
ARG SIGNALWIRE_SPACE
ENV SIGNALWIRE_SPACE=${SIGNALWIRE_SPACE}
ARG PROJECT_ID
ENV PROJECT_ID=${PROJECT_ID}
ARG REST_API_TOKEN
ENV REST_API_TOKEN=${REST_API_TOKEN}
ARG VISUAL
ENV VISUAL=${VISUAL}
ARG LOCALTONET_API_TOKEN
ENV LOCALTONET_API_TOKEN=${LOCALTONET_API_TOKEN}
ARG LOCALTONET_AUTH_TOKEN
ENV LOCALTONET_AUTH_TOKEN=${LOCALTONET_AUTH_TOKEN}
ARG WORKDIR
ENV WORKDIR=${WORKDIR}

# Install the basic package
RUN apt update && apt install -y apache2 screen jq curl wget less git gawk lsb-release ca-certificates gnupg unzip

# Install Editors
RUN apt update && apt install -y nano vim emacs-nox

# Install Python
RUN apt update && apt install -y python3 python3-pip && pip3 install signalwire requests python-dotenv cmd2 setuptools

# Install golang
#RUN apt update && apt install -y golang 

# Install PHP
#RUN apt update && apt install -y php-cli composer 

# Install GH Cli
RUN apt-key adv --fetch-keys https://cli.github.com/packages/githubcli-archive-keyring.gpg && echo "deb [arch=$(dpkg --print-architecture)] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list && \
    apt update && apt install -y gh

# Install Docker 
RUN apt-key adv --fetch-keys https://download.docker.com/linux/debian/gpg && echo "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list && \
    apt update && apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Install Ngrok
# TODO eventually may want to change this to not use curl and remove curl from the image.
RUN apt-key adv --fetch-keys https://ngrok-agent.s3.amazonaws.com/ngrok.asc && echo "deb [arch=$(dpkg --print-architecture)] https://ngrok-agent.s3.amazonaws.com $(lsb_release -cs) main" |  tee /etc/apt/sources.list.d/ngrok.list && \
    apt update && apt install -y ngrok 

# Install localtonet
RUN export LOCALTONETARCH=`uname -m | sed 's/aarch64/arm64/g' | sed 's/x86_64/x64/g'` && wget https://www.localtonet.com/download/localtonet-linux-${LOCALTONETARCH}.zip && unzip localtonet-linux-${LOCALTONETARCH}.zip && mv localtonet /usr/bin/ && \
    rm -f localtonet-linux-${LOCALTONETARCH}.zip && chmod 755 /usr/bin/localtonet

# Install NVM 
RUN curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash

# Enable Python -- Apache
# This may need to just be creating the symlink since the image doesn't run
RUN a2enmod cgid

# Configure Ngrok
RUN if [ ! -z "${NGROK_TOKEN}" ]; then ngrok config add-authtoken $NGROK_TOKEN; fi

# Install Docker examples
COPY examples /root/examples

# Copy files to /opt/signalwire
RUN pwd
COPY docker/SRC /usr/lib/cgi-bin
COPY docker/SRC/foo_laml.xml.orig /tmp/.foo_laml.xml.orig
RUN chmod +x -R /usr/lib/cgi-bin/

# copy script to start services
COPY docker/start_services.sh /root/start_services.sh
RUN chmod +x /root/start_services.sh

# Copy in VARS 
COPY .env /usr/lib/cgi-bin/.env

# Make workdir
RUN mkdir -p /workdir/public

#Create public web folder
RUN ln -s /workdir/public/ /var/www/html/public

# Start the user in swsh
RUN echo "python3 /usr/lib/cgi-bin/swsh.py" >> /root/.bashrc
RUN ln -s /usr/lib/cgi-bin/swsh.py /usr/bin/swsh

WORKDIR /workdir

# Start Apache and ngrok on container start
ENTRYPOINT sed -i -e 's/\r$//' /root/start_services.sh && /root/start_services.sh && /bin/bash
