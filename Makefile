
front:
	$(MAKE) -C frontend dev

back:
	$(MAKE) -C backend dev

stop:
	docker-compose stop

build:
	docker-compose up -d --build

deploy:
	docker-compose up