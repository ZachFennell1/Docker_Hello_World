# Name the node stage "builder"
FROM alpine:latest AS build-stage
USER root
WORKDIR /app
COPY . .

# production stage
FROM alpine:latest

RUN mkdir -p /www
COPY --from=build-stage /app /www

RUN apk add --no-cache bash
RUN apk add nginx openrc gettext --no-cache
RUN addgroup www
RUN adduser -D -h /www -G 'www' www
RUN mkdir -p /var/cache/nginx
RUN chown -R www:www /var/lib/nginx
RUN chown -R www:www /www


COPY ./nginx.conf /etc/nginx/nginx.conf
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]