# MAINTAINER: support@signalwire.com
#TODO:
# - Install other SDKs 
# - Variablize the space name and API Key
# - Research how to take API key and made Basic Auth Header

FROM debian:12.11-slim

ARG python_version=python3.11

# Install the basic packages (includes man-db for man pages)
RUN apt update && apt install -y screen tmux jq curl wget less git gawk lsb-release ca-certificates gnupg unzip dos2unix bind9-dnsutils bind9-dnsutils libjson-perl perl-doc libcgi-pm-perl libtest-lwp-useragent-perl liburl-encode-perl libfile-slurp-perl libuuid-perl libyaml-perl cpanminus libpq-dev ca-certificates nginx postgresql-all sudo whiptail pkg-config libgd-dev redis-server inotify-tools ffmpeg sox sqlite3 ncdu man-db 

# Install Editors
RUN apt update && apt install -y nano vim emacs-nox micro ne

# Install Python and dev tools (includes uv/uvx - fast Python package manager)
RUN apt update && apt install -y python3 python3-pip python3.11-venv && pip3 install --upgrade --break-system-packages signalwire requests python-dotenv cmd2 setuptools pygments swsh flask signalwire-agents signalwire-swml signalwire-swaig signalwire-pom ipython httpie watchdog black build twine uv

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

# Install Cloudflare Tunnel
RUN mkdir -p --mode=0755 /usr/share/keyrings \
    && curl -fsSL https://pkg.cloudflare.com/cloudflare-public-v2.gpg | tee /usr/share/keyrings/cloudflare-public-v2.gpg > /dev/null \
    && echo "deb [signed-by=/usr/share/keyrings/cloudflare-public-v2.gpg] https://pkg.cloudflare.com/cloudflared any main" | tee /etc/apt/sources.list.d/cloudflared.list > /dev/null \
    && apt update \
    && apt install -y cloudflared

# Install Node.js 20 for AI CLI tools
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt install -y nodejs

# Install Claude Code, Gemini CLI, and OpenAI Codex CLI
RUN npm install -g @anthropic-ai/claude-code @google/gemini-cli @openai/codex

# Install Ollama CLI (for connecting to Ollama running on host)
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install AWS CLI v2
RUN curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-$(uname -m).zip" -o /tmp/awscliv2.zip \
    && unzip -q /tmp/awscliv2.zip -d /tmp \
    && /tmp/aws/install \
    && rm -rf /tmp/aws /tmp/awscliv2.zip

# Install Google Cloud CLI
RUN curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee /etc/apt/sources.list.d/google-cloud-sdk.list \
    && apt update \
    && apt install -y google-cloud-cli

# Install Azure CLI
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/azure-cli.list \
    && apt update \
    && apt install -y azure-cli

# Install encryption tools (git-crypt, age, SOPS) for secrets management
RUN apt update && apt install -y git-crypt \
    && ARCH=$(dpkg --print-architecture) \
    && curl -fsSL "https://github.com/FiloSottile/age/releases/download/v1.2.0/age-v1.2.0-linux-${ARCH}.tar.gz" \
       | tar -xz -C /usr/local/bin --strip-components=1 age/age age/age-keygen \
    && curl -fsSL "https://github.com/getsops/sops/releases/download/v3.9.0/sops-v3.9.0.linux.${ARCH}" \
       -o /usr/local/bin/sops && chmod +x /usr/local/bin/sops

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

# Install WireStarter man page
COPY misc/wirestarter.1 /usr/share/man/man1/wirestarter.1
RUN gzip -f /usr/share/man/man1/wirestarter.1 && mandb -q
# Clean up
RUN /usr/bin/dos2unix /root/.bashrc         # Fixes DOS formatting when using Windows
RUN /usr/bin/dos2unix /start_services.sh    # Fixes DOS formatting when using Windows
RUN apt clean

WORKDIR /workdir

# Start ngrok on container start
ENTRYPOINT ["/start_services.sh"]
