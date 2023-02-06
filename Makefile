make: build run

debug: build
	docker compose up

build: 
	docker compose build 

run: 
	docker compose up -d

clean: stop
	docker rm microtest-broker microtest-hello microtest-world microtest-frontend microtest-dns

stop: 
	docker stop microtest-broker microtest-frontend microtest-hello microtest-world microtest-dns


