# production stage
FROM alpine:latest
USER root
WORKDIR /app
RUN apk add --no-cache python3 py3-pip
RUN apk add --no-cache bash

COPY . .
RUN adduser -D brokeruser
RUN chown -R brokeruser /app
RUN chmod +x server.py

USER brokeruser
ENV PYTHONUNBUFFERED=true
ENV PATH="$PATH:/home/brokeruser/.local/bin"