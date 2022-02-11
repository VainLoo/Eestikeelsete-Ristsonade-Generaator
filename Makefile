front-prod-build:
	$(MAKE) -C frontend prod-build

front-up:
	$(MAKE) -C frontend front-up

front-prod-up:
	$(MAKE) -C frontend front-prod-up

front-stop:
	$(MAKE) -C frontend front-stop

back-up:
	$(MAKE) -C backend back-up

back-stop:
	$(MAKE) -C backend back-stop

all-up:
	make front-up
	make back-up
	
all-stop:
	make back-stop
	make front-stop

make build:
	docker-compose up -d --build