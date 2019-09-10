help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build:	## Build the package
	docker-compose -f docker-compose.yml build --no-cache


up:	## Start production deployment
	docker-compose -f docker-compose.yml up

clean: ## WARNING! Deletes all volumes so you can start the DB from blank
	docker volume prune -f
