FROM alpine:latest
USER root
WORKDIR /app
RUN apk add --no-cache python3 py3-pip
RUN apk add --no-cache bash

COPY . .
RUN adduser -D dnsuser
RUN chown -R dnsuser /app
RUN chmod +x server.py

USER dnsuser
RUN touch namefile

ENV PYTHONUNBUFFERED=true
ENV PATH="$PATH:/home/dnsuser/.local/bin"