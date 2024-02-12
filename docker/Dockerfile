# MAINTAINER: support@signalwire.com
#TODO:
# - Install other SDKs 
# - Variablize the space name and API Key
# - Research how to take API key and made Basic Auth Header

FROM debian:12-slim

ARG python_version=python3.9

# Install the basic package
RUN apt update && apt install -y screen jq curl wget less git gawk lsb-release ca-certificates gnupg unzip dos2unix bind9-dnsutils bind9-dnsutils libjson-perl perl-doc libcgi-pm-perl libtest-lwp-useragent-perl liburl-encode-perl libfile-slurp-perl libuuid-perl libyaml-perl cpanminus libpq-dev ca-certificates 

# Install Editors
RUN apt update && apt install -y nano vim emacs-nox

# Install Python
RUN apt update && apt install -y python3 python3-pip && pip3 install --break-system-packages signalwire requests python-dotenv cmd2 setuptools pygments swsh



# Install Docker
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | tee /etc/apt/trusted.gpg.d/docker.asc > /dev/null \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/trusted.gpg.d/docker.asc] https://download.docker.com/linux/debian  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt update \
    && apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/etc/apt/trusted.gpg.d/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-b7=/etc/apt/trusted.gpg.d/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github.list > /dev/null \
    && apt update \
    && apt install -y gh

RUN curl -fsSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc |  tee /etc/apt/trusted.gpg.d/ngrok.asc > /dev/null \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/trusted.gpg.d/ngrok.asc] https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list > /dev/null \
    && apt update \
    && apt install -y ngrok

RUN pwd
COPY docker/SRC /usr/lib/cgi-bin
COPY docker/SRC/foo_laml.xml.orig /tmp/.foo_laml.xml.orig
RUN chmod +x -R /usr/lib/cgi-bin/

# copy script to start services
COPY docker/start_services.sh /start_services.sh
RUN chmod +x /start_services.sh

# Make workdir
RUN mkdir -p /workdir/public
RUN mkdir -p /var/www/html/public

#Create public web folder
RUN ln -s /workdir/public/ /var/www/html/public

# Misc
COPY misc/signalwire.ans /.sw.ans
COPY misc/bash.rc /root/.bashrc
COPY bin/ /usr/bin

# Clean up
RUN /usr/bin/dos2unix /root/.bashrc         # Fixes DOS formatting when using Windows
RUN /usr/bin/dos2unix /start_services.sh    # Fixes DOS formatting when using Windows
RUN rm -f /tmp/cmd2.patch
RUN rm -f /tmp/pygment_mapping.patch
RUN apt clean

# Copy file to redirect to documentation
COPY www/ /var/www/html/

WORKDIR /workdir

# Start and ngrok on container start
ENTRYPOINT /start_services.sh
