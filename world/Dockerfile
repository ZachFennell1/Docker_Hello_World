FROM alpine:latest
USER root
WORKDIR /app
RUN apk add --no-cache python3 py3-pip
RUN apk add --no-cache bash

COPY . .
RUN adduser -D worlduser
RUN chown -R worlduser /app
RUN chmod +x server.py

USER worlduser
ENV PYTHONUNBUFFERED=true
ENV PATH="$PATH:/home/worlduser/.local/bin"