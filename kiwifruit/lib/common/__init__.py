from kiwifruit.lib.core.config import MYSQL_HOST, MYSQL_DATABASE, MYSQL_USERNAME, MYSQL_PASSWD, MYSQL_PORT
from kiwifruit.lib.common import kwfdb

_host = "%s:%s" % (MYSQL_HOST, MYSQL_PORT)

db = kwfdb.Connection(_host, MYSQL_DATABASE, MYSQL_USERNAME, MYSQL_PASSWD)
