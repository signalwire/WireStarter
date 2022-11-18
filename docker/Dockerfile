# MAINTAINER: support@signalwire.com
#TODO:
# - Install other SDKs 
# - Variablize the space name and API Key
# - Research how to take API key and made Basic Auth Header

FROM debian:bullseye-slim

# Install the basic package
RUN apt update && apt install -y apache2 screen jq curl wget less git gawk lsb-release ca-certificates gnupg unzip dos2unix

# Install Editors
RUN apt update && apt install -y nano vim emacs-nox

# Install Python
RUN apt update && apt install -y python3 python3-pip && pip3 install signalwire requests python-dotenv cmd2 setuptools pygments typing-extensions

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

# Copy patch for Cmd2 and patch the file
# Allows persistant history behavior by default 
# Allows for adding env vars into the shell 
# At some point, rather than patch, we may just want to copy in our own version of the module, if it becomes too messy.
# -Shane.
COPY misc/cmd2.patch /tmp/cmd.patch
RUN /usr/bin/patch /usr/local/lib/${PYTHON_VER}/dist-packages/cmd2/cmd2.py  < /tmp/cmd2.patch

# Copy Patch to allow 'nicer' coloring on JSON output 
# Creats a new formatter called SwishFormatter that can be used to customize any coloring
COPY misc/swishcolor.py /usr/local/lib/${PYTHON_VER}/dist-packages/pygments/formatters/swishcolor.py
COPY misc/pygment_mapping.patch /tmp/pygment_mapping.patch
RUN /usr/bin/patch /usr/local/lib/${PYTHON_VER}/dist-packages/pygments/formatters/_mapping.py < /tmp/pygment_mapping.patch

# Clean up
RUN /usr/bin/dos2unix /root/.bashrc         # Fixes DOS formatting when using Windows
RUN /usr/bin/dos2unix /start_services.sh    # Fixes DOS formatting when using Windows
RUN rm -f /tmp/cmd2.patch
RUN rm -f /tmp/pygment_mapping.patch
RUN apt clean

# Start the user in swsh
RUN ln -s /usr/lib/cgi-bin/swsh.py /usr/bin/swsh

# Copy file to redirect to documentation
COPY www/ /var/www/html/

WORKDIR /workdir

# Fix ports
RUN sed -i -e 's/Listen 80/Listen 9080/' /etc/apache2/ports.conf
RUN sed -i -e 's/Listen 443/Listen 9443/' /etc/apache2/ports.conf

# Start Apache and ngrok on container start
ENTRYPOINT /start_services.sh
