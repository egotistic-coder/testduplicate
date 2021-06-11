import os
import urllib

host_server = os.environ.get('host_server')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port')))
database_name = os.environ.get('database_name')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode')))
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)