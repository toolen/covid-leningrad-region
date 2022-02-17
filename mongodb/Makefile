restore:
	docker exec -i mongo sh -c 'exec mongorestore \
	--ssl --sslCAFile=/data/ssl/ca.pem \
	--sslPEMKeyFile=/data/ssl/mongo.pem \
	--authenticationDatabase "$external" \
	--authenticationMechanism MONGODB-X509 \
	--archive' < dump/covid_stat/leningrad_region.archive