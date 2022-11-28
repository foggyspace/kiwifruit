from libs.core.settings import MYSQL_HOST,MYSQL_PORT,MYSQL_USERNAME,MYSQL_PASSWD,MYSQL_DATABASE

import db as mdb

_host = "%s:%s" % (MYSQL_HOST,MYSQL_PORT)
db = mdb.Connection(_host,MYSQL_DATABASE,MYSQL_USERNAME,MYSQL_PASSWD)
