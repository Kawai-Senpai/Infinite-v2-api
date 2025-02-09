docker run -p 9000:9000 --env ENVIRONMENT=testing --env-file .env.testing --add-host=host.docker.internal:host-gateway infinite-api
