FROM alpine:latest
USER root
WORKDIR /app
RUN apk add --no-cache python3 py3-pip
RUN apk add --no-cache bash

COPY . .
RUN adduser -D hellouser
RUN chown -R hellouser /app
RUN chmod +x server.py

USER hellouser
ENV PYTHONUNBUFFERED=true
ENV PATH="$PATH:/home/hellouser/.local/bin"