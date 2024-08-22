import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()  # Load environment variables from .env file

#MYSQL_HOST=os.getenv("MYSQL_HOST") # Use this if you containerize your app
MYSQL_HOST="localhost"

MYSQL_USER=os.getenv("MYSQL_USER")
MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")
MYSQL_DB=os.getenv("MYSQL_DB")

# Check Docker Logs for MySQL, example:
"""
2024-08-22 13:15:18 2024-08-22T11:15:18.285380Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.39'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
"""

# SQLite database file path
connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{3306}/{MYSQL_DB}'

engine = create_engine(connection_string, echo=True)

