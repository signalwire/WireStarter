FROM python:3.9

ARG PROJECT_ID
ENV PROJECT_ID=${PROJECT_ID}
ARG API_TOKEN
ENV API_TOKEN=${API_TOKEN}

RUN pip install signalwire python-dotenv
COPY start.py .
CMD [ "python", "./start.py" ]
