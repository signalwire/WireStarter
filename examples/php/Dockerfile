FROM debian:buster-slim

ARG PROJECT_ID
ENV PROJECT_ID=${PROJECT_ID}
ARG API_TOKEN
ENV API_TOKEN=${API_TOKEN}
RUN apt update && apt install -y php-cli composer
RUN composer require signalwire/signalwire
COPY start.php .
CMD [ "php", "./start.php" ]
