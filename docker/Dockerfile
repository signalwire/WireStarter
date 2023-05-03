# MAINTAINER: support@signalwire.com
#TODO:
# - Install other SDKs 
# - Variablize the space name and API Key
# - Research how to take API key and made Basic Auth Header

FROM debian:bullseye-slim

ARG python_version=python3.9

# Install the basic package
RUN apt update && apt install -y apache2 screen jq curl wget less git gawk lsb-release ca-certificates gnupg unzip dos2unix bind9-dnsutils bind9-dnsutils libjson-perl perl-doc libcgi-pm-perl libtest-lwp-useragent-perl

# Install Editors
RUN apt update && apt install -y nano vim emacs-nox

# Install Python
RUN apt update && apt install -y python3 python3-pip && pip3 install signalwire requests python-dotenv cmd2 setuptools pygments swsh

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
RUN apt-key adv --fetch-keys https://ngrok-agent.s3.amazonaws.com/ngrok.asc && echo "deb [arch=$(dpkg --print-architecture)] https://ngrok-agent.s3.amazonaws.com $(lsb_release -cs) main" |  tee /etc/apt/sources.list.d/ngrok.list && \
    apt update && apt install -y ngrok 

# Enable Python -- Apache
# This may need to just be creating the symlink since the image doesn't run
RUN a2enmod cgid

# Install Docker examples
COPY examples /root/examples

RUN pwd
COPY docker/SRC /usr/lib/cgi-bin
COPY docker/SRC/foo_laml.xml.orig /tmp/.foo_laml.xml.orig
RUN chmod +x -R /usr/lib/cgi-bin/

# copy script to start services
COPY docker/start_services.sh /start_services.sh
RUN chmod +x /start_services.sh

# Make workdir
RUN mkdir -p /workdir/public

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

# Enable CGI
RUN sed -i -e 's/#AddHandler cgi-script .cgi/AddHandler cgi-script .cgi/' /etc/apache2/mods-available/mime.conf

# Fix ports
RUN sed -i -e 's/Listen 80/Listen 9080/' /etc/apache2/ports.conf
RUN sed -i -e 's/Listen 443/Listen 9443/' /etc/apache2/ports.conf

# Start Apache and ngrok on container start
ENTRYPOINT /start_services.sh
