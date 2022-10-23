FROM python:3.9

ARG PROJECT_ID
ENV PROJECT_ID=${PROJECT_ID}
ARG REST_API_TOKEN
ENV REST_API_TOKEN=${REST_API_TOKEN}

RUN pip install signalwire python-dotenv
COPY start.py .
CMD [ "python", "./start.py" ]
