# 插件相关配置
PLUGINS_DIR = 'plugins'

# 字典相关配置
DICT_DIR = 'dics'
WEBSHELL_DIC = 'webshell.dic'

# 编码配置
DEFAULT_ENCODING = 'utf-8'

# 忽略的文件后缀
IGNORE_DEFAULT_FILE_SUFFIX = ('jpg','png','jpeg','png','jpg','gif','bmp','svg',
                            'exe','rar','zip',
                            'js','css')

# 日志配置
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = 'kiwifruit.log'

# 安全配置
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# 扫描配置
SCAN_TIMEOUT = 300  # 5分钟
MAX_SCAN_DEPTH = 3
MAX_SCAN_URLS = 1000

# 缓存配置
CACHE_TYPE = 'redis'
CACHE_REDIS_URL = 'redis://localhost:6379/2'
CACHE_DEFAULT_TIMEOUT = 300
