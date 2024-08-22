# sqlalchemy-demo
This is my notebook repo for reading up on SQLAlchemy

## Tutorial MySQL in Docker: 
## https://docs.docker.com/get-started/workshop/07_multi_container/

# Setup/start MySQL in Docker:
docker compose up --build -d

### Verify that the MySQL is up and running:
`docker exec -it <mysql-container-id> mysql -u root -p`
When the password prompt comes up, type in `secret`. In the MySQL shell, list the databases and verify you see the `alchemy` database.
<br>

List the databases and verify you see the alchemy database:
`mysql> SHOW DATABASES;`

If all is well, exit the MySQL shell by typing:
`mysql> exit`


# Connect to MySQL



# Build the Docker image:
docker build -t sqlalchemy-demo .

# Run the Docker image:
docker run -dp 127.0.0.1:3000:3000 --name sqlalchemy-unified-tutorial --mount type=volume,src=sqlalchemy-demo.db,target=/etc/sqlalchemy-demo sqlalchemy-demo