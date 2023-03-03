from lib.core.settings import MYSQL_HOST,MYSQL_PORT,MYSQL_USERNAME,MYSQL_PASSWD,MYSQL_DATABASE

from lib.db import endb as mydb


_host = f"{MYSQL_HOST}:{MYSQL_PORT}"

db = mydb.Connection(_host,MYSQL_DATABASE,MYSQL_USERNAME,MYSQL_PASSWD)
