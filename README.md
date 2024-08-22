# sqlalchemy-demo
This is my "notebook" repo for reading up on [this SQLAlchemy tutorial](https://docs.docker.com/get-started/workshop/07_multi_container/)

# Setup/start MySQL in Docker:
docker compose up --build -d

### Verify that the MySQL is up and running:
1) Find the correct Container ID for MySQL: `docker ps` 
2) `docker exec -it <mysql-container-id> mysql -u root -p`
* When the password prompt comes up, type in `secret`. 
* In the MySQL shell, list the databases and verify you see the `alchemy` database.
<br>

3) List the databases and verify you see the alchemy database:
* mysql> `SHOW DATABASES;`
* If all is well, exit the MySQL shell by typing: mysql> `exit`

# Connect to MySQL
The `compose.yaml`is exposing the MySQL container port to the same localhost port. See keys.py for connection string.

### Now what?
You've got yourself a persistent MySQL database where you can play along with the SQLAlchemy tutorial, instead of only having an "in-memory-database".