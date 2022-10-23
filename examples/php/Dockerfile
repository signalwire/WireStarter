FROM debian:buster-slim

ARG PROJECT_ID
ENV PROJECT_ID=${PROJECT_ID}
ARG REST_API_TOKEN
ENV REST_API_TOKEN=${REST_API_TOKEN}
RUN apt update && apt install -y php-cli composer
RUN composer require signalwire/signalwire
COPY start.php .
CMD [ "php", "./start.php" ]
