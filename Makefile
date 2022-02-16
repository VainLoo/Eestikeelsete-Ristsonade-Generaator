
front:
	$(MAKE) -C frontend dev

back:
	$(MAKE) -C backend dev

stop:
	docker-compose stop

prod:
	docker-compose up -d --build

deploy:
	docker-compose up

dev:
	docker-compose -f docker-compose.yml -f docker-compose-development.yml up -d --build