#from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor


executors = {
        'default': ThreadPoolExecutor(20)
}
