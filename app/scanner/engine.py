import gevent
from gevent import pool, queue, spawn, joinall


class ScanEgine(object):
    def __init__(self, task_id: int) -> None:
        self.pool: pool.Pool = pool.Pool(10)
        self.task_id = task_id
        self.host = ''


    def start(self) ->None:
        joinall([
            spawn(self.schedulerURL)
        ])

        self.pool.join()

    def schedulerURL(self) -> None:
        pass

    def schedulerDomain(self) -> None:
        pass



def run(task_id: int) -> None:
    engine = ScanEgine(task_id)
    engine.start()

