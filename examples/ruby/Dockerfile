FROM ruby:3.1.2-buster

ARG PROJECT_ID
ENV PROJECT_ID=${PROJECT_ID}
ARG API_TOKEN
ENV API_TOKEN=${API_TOKEN}

RUN gem install nokogiri --platform=ruby -- --use-system-libraries
RUN gem install signalwire

COPY start.rb .
CMD [ "ruby", "./start.rb" ]
