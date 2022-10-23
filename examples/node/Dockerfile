FROM node:current-buster-slim

ARG PROJECT_ID
ENV PROJECT_ID=${PROJECT_ID}
ARG REST_API_TOKEN
ENV REST_API_TOKEN=${REST_API_TOKEN}

RUN mkdir /app
WORKDIR /app
RUN npm install @signalwire/realtime-api
COPY start.js .
CMD [ "node", "start.js" ]
