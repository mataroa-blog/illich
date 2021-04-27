#!/usr/bin/env bash

cd /opt/apps/illich
source .envrc
pg_dump -Fc --no-acl illich -h localhost -U illich -f /home/illich/illich.dump -w
/usr/local/bin/aws s3 cp /home/illich/illich.dump s3://mataroa/illich-backups/postgres-illich-$(date --utc +%Y-%m-%d-%H-%M-%S)/
