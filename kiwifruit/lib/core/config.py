HEADERS = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0'
}

HEADER_BODY_BOUNDRY = ""

IGNORE_DEFAULT_FILE_SUFFIX = ('jpg','png','jpeg','png','jpg','gif','bmp','svg',
                            'exe','rar','zip',
                            'js','css')


MYSQL_HOST = "xxxxxx"
MYSQL_PORT = 3306
MYSQL_USERNAME = "test"
MYSQL_PASSWD = "test"
MYSQL_DATABASE = "kehan"

TASK_TABLE = 'task'
RULE_TABLE = "rule"
URL_TABLE = "url"
RESULT_TABLE = "result"
RUN_URL_DEFAULT_FUN = "run_url"
RUN_DOMAIN_DEFAULT_FUN = "run_domain"


SCRIPTS_NAME = "scripts"     #规则目录
SCRIPTS_DIC_NAME = "dic" #字典目录
#TEMP_NAME = "temp"  #缓存文件
TEMP_NAME = "temp"
LOG_NAME = "toplog.log"

################## gloabl default setting ##################
DEFAULT_PAGE_ENCODING = "utf8"
HEADER_BODY_BOUNDRY = ""

################## cmdline default setting ##################
# may change by cmdline
CONNECTION_TIMEOUT = 10
NETWORK_TIMEOUT = 10