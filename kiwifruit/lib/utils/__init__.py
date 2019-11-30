from lib.core.settings import (MYSQL_HOST, MYSQL_PORT, MYSQL_USERNAME,
MYSQL_PASSWORD, MYSQL_DATABASE)

import torndb

_host = "%s:%s" % (MYSQL_HOST, MYSQL_PORT)
db = torndb.Connection(_host, MYSQL_DATABASE, MYSQL_USERNAME, MYSQL_PASSWORD)

