# Celery配置文件

# Broker配置，使用Redis作为消息中间件
broker_url = 'redis://localhost:6379/0'

# Backend配置，使用Redis作为结果后端
result_backend = 'redis://localhost:6379/1'

# 任务序列化方式
task_serializer = 'json'

# 结果序列化方式
result_serializer = 'json'

# 接受的内容类型
accept_content = ['json']

# 时区设置
timezone = 'Asia/Shanghai'

# 是否使用UTC
enable_utc = False

# 任务结果过期时间
result_expires = 3600  # 1小时

# 任务的硬时间限制，超时会被终止
task_time_limit = 3600  # 1小时

# 任务的软时间限制，超时会发出警告
task_soft_time_limit = 3000  # 50分钟

# 工作进程并发数
worker_concurrency = 4

# 每个工作进程预取的任务数
worker_prefetch_multiplier = 4

# 任务默认速率限制
task_default_rate_limit = '10/s'