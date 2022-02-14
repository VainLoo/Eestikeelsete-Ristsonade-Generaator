front-up:
	docker-compose up -d --build

prod-build:
	docker build -f Dockerfile.prod -t sample:prod .

prod-up:
	docker-compose -f docker-compose.prod.yml up -d --build

dev:
	npm start