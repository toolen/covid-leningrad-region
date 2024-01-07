mongodb
=======================

To restore database:

1. Unzip dump/covid_stat/leningrad_region.archive.tar.gz
2. Run docker-compose
3. Connect to mongo container
4. Go to /data/dump/covid_stat
5. Execute:

```
mongorestore \
--ssl --sslCAFile=/data/ssl/ca.pem \
--sslPEMKeyFile=/data/ssl/mongo.pem \
--authenticationDatabase "$external" \
--authenticationMechanism MONGODB-X509 \
--archive < leningrad_region.archive
```
