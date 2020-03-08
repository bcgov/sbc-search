# sbc-search
BC Registries and Online Services search services

## Project setup (Docker)

Development

Install Oracle instantclient libs, currently outside Docker.

TODO: automatically download these, but have to deal with changing version numbers:
```
wget https://download.oracle.com/otn_software/linux/instantclient/19600/instantclient-basic-linux.x64-19.6.0.0.0dbru.zip
unzip instantclient-basic-linux.x64-19.6.0.0.0dbru.zip
https://download.oracle.com/otn_software/linux/instantclient/19600/instantclient-sdk-linux.x64-19.6.0.0.0dbru.zip
unzip instantclient-sdk-linux.x64-19.6.0.0.0dbru.zip
mv instantclient_19_6 instantclient
```

set docker compose config
```
cp dc.dev.yml docker-compose.override.yml
cp frontend/example.env frontend/.env
docker-compose up
```
Browse to `localhost:8080`

Deployment
```
cp dc.prod.yml docker-compose.override.yml
docker-compose up
```
Browse to `localhost:8080`

Updating database and create mock data
```
dx search_api (in nother terminal, to access the container)
flask db upgrade (to run existing migrations and update de db)
python bootstrap.py to create mock data
```

## connecting to the dev database

Connect to VPN

Download [cisco VPN client](https://software.cisco.com/download/home/286281283/type/282364313/release/4.7.04056?i=!pp)

```
cd /opt
tar zxvf anyconnect-linux64-4700136-predeploy-k9tar.gz
cd anyconnect*/bin
vpn
>> connect vpn2.gov.bc.ca
```
(enter your IDIR username and password)

Install `ncat` to enable port-forwarding. (Note: depending on your version of `nmap` you may need to install both `nmap` and `ncat`, or just `nmap`.)

```
apt-get install nmap ncat
ncat -l 0.0.0.0 1521 --keep-open --sh-exec "ncat nettle.bcgov 1521"
```

set your search-api/.env database URL to `DB_CONNECTION_URL=oracle://$USERNAME:$PASSWORD@$DOCKER_IP:1521/CDEV`

WHERE $USERNAME and $PASSWORD are read only dev db creds, and $DOCKER_IP is findable from running `ip addr show` in your search_api container, and changing the last digit to 1. It's a refrence to your HOST's IP from inside your container, typically such as 172.1.0.1 .

## Migrations

This project uses
  * [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/)
  * [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/), based on alembic.

These operations are done in the search_api container

To initially get your DB up to date:
```
flask db upgrade
```

To create new migration scripts
```
flask db migrate
git add
```


