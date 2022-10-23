FROM node:current-buster-slim

ARG PROJECT_ID
ENV PROJECT_ID=${PROJECT_ID}
ARG API_TOKEN
ENV API_TOKEN=${API_TOKEN}

RUN mkdir /app
WORKDIR /app
RUN npm install @signalwire/realtime-api
COPY start.js .
CMD [ "node", "start.js" ]
#CMD bash
