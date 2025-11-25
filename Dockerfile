# MAINTAINER: support@signalwire.com
#TODO:
# - Install other SDKs 
# - Variablize the space name and API Key
# - Research how to take API key and made Basic Auth Header

FROM debian:12.11-slim

ARG python_version=python3.11

# Install the basic packages
RUN apt update && apt install -y screen jq curl wget less git gawk lsb-release ca-certificates gnupg unzip dos2unix bind9-dnsutils bind9-dnsutils libjson-perl perl-doc libcgi-pm-perl libtest-lwp-useragent-perl liburl-encode-perl libfile-slurp-perl libuuid-perl libyaml-perl cpanminus libpq-dev ca-certificates nginx postgresql-all sudo whiptail pkg-config libgd-dev redis-server inotify-tools ffmpeg sox sqlite3 ncdu 

# Install Editors
RUN apt update && apt install -y nano vim emacs-nox

# Install Python and dev tools
RUN apt update && apt install -y python3 python3-pip python3.11-venv && pip3 install --upgrade --break-system-packages signalwire requests python-dotenv cmd2 setuptools pygments swsh flask signalwire-agents signalwire-swml signalwire-swaig signalwire-pom ipython httpie watchdog black build twine

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

# Install Node.js 20 for AI CLI tools
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt install -y nodejs

# Install Claude Code and Gemini CLI
RUN npm install -g @anthropic-ai/claude-code @google/gemini-cli

RUN pwd
COPY misc/foo_laml.xml.orig /tmp/.foo_laml.xml.orig

# CLONE AI STARTER PACK
RUN git clone https://github.com/signalwire/ai-agent-starter-pack.git /usr/local/ai-agent-starter-pack

# copy script to start services
COPY misc/start_services.sh /start_services.sh
RUN chmod +x /start_services.sh

# Make workdir
RUN mkdir -p /workdir/public

#Create public web folder
RUN ln -s /workdir/public/ /var/www/html/public

# Misc
COPY misc/signalwire.ans /.sw.ans
COPY misc/bash.rc /root/.bashrc
COPY bin/ /usr/bin
COPY conf/nginx.site /etc/nginx/sites-enabled/default
# Clean up
RUN /usr/bin/dos2unix /root/.bashrc         # Fixes DOS formatting when using Windows
RUN /usr/bin/dos2unix /start_services.sh    # Fixes DOS formatting when using Windows
RUN apt clean

WORKDIR /workdir

# Start ngrok on container start
ENTRYPOINT /start_services.sh
