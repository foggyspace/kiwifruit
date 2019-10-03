from __future__ import absolute_import, division, with_statement

import copy
import logging
import os
import time

try:
    import MySQLdb.constants
    import MySQLdb.converters
    import MySQLdb.cursors
except ImportError:
    if "READTHEDOCS" in os.environ:
        MySQLdb = None
    else:
        raise


version = "0.2"
version_info = (0, 2, 0, 0)

CONVERSIONS = None


class Connection(object):
    def __init__(self, host, database,
                 user=None, password=None,
                 max_idle_time=7*3600,
                 connect_timeout=0,
                 time_zone="+0:00",
                 charset="utf-8",
                 sql_mode="TRADITIONAL"):
        self.host = host
        self.database = database
        self.max_idle_time = float(max_idle_time)

        args = dict(
            conv=CONVERSIONS,
            use_unicode=True,
            charset=charset,
            db=database,
            init_command=("SET time_zone = `%s`" % time_zone),
            connect_timeout=connect_timeout,
            sql_mode=sql_mode
        )

        if user is not None:
            args["user"] = user

        if password is not None:
            args["password"] = password

        if "/" in host:
            args["unix_socket"] = host
        else:
            self.socket = None
            pair = host.split(":")
            if len(pair) == 2:
                args["host"] = pair[0]
                args["port"] = int(pair[1])
            else:
                args["host"] = host
                args["port"] = 3306

        self._db = None
        self._db_args = args
        self._last_use_time = time.time()

        try:
            self.reconnect()
        except Exception:
            logging.error("[-] Cannot connect to Mysql on %s" % self.host, exc_info=True)

    def __del__(self):
        self.close()

    def close(self):
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def reconnect(self):
        self.close()
        self._db = MySQLdb.connect(**self._db_args)
        self._db.autocommit(True)

    def iter(self, query, *parameters, **kw_parameters):
        self._ensure_connected()
        cursor = MySQLdb.cursors.SSCursor(self._db)
        try:
            self._execute(cursor, query, parameters, kw_parameters)
            columns_names = [d[0] for d in cursor.description]
            for row in cursor:
                yield Row(zip(columns_names, row))
        finally:
            cursor.close()

    def query(self, query, *parameters, **kw_parameters):
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kw_parameters)
            column_names = [d[0] for d in cursor.description]
            return [Row(zip(column_names, row)) for row in cursor]
        finally:
            cursor.close()

    def get(self, query, *parameters, **kw_parameters):
        rows = self.query(query, *parameters, **kw_parameters)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("[-] Multiple rows returned for Database.get() query")
        else:
            return rows[0]

    def execute(self, query, *parameters, **kw_parameters):
        return self.execute_lastrowid(query, *parameters, **kw_parameters)

    def execute_lastrowid(self, query, *parameters, **kw_parameters):
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kw_parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def execute_rowcount(self, query, *parameters, **kw_parameters):
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kw_parameters)
            return cursor.rowcount()
        finally:
            cursor.close()

    def executemany(self, query, parameters):
        return self.execute_lastrowid(query, parameters)

    def executemany_lastrowid(self, query, parameters):
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def executemany_rowcount(self, query, parameters):
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    update = execute_rowcount
    update_many = executemany_rowcount

    insert = execute_lastrowid
    insert_many = executemany_lastrowid


    def _ensure_connected(self):
        if (self._db is None or (time.time() - self._last_use_time > self.max_idle_time)):
            self.reconnect()
        self._last_use_time = time.time()

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()

    def _execute(self, cursor, query, *parameters, **kw_parameters):
        try:
            return cursor.execute(query, kw_parameters or parameters)
        except OperationalError:
            logging.error("[-] Error connection to Mysql on %s" % self.host)
            self.close()
            raise


class Row(object):
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item)

if MySQLdb is not None:
    FIELD_TYPE = MySQLdb.constants.FIELD_TYPE
    FLAG = MySQLdb.constants.FLAG
    CONVERSIONS = copy.copy(MySQLdb.converters.converters)

    field_types = [FIELD_TYPE.BLOB, FIELD_TYPE.STRING, FIELD_TYPE.VAR_STRING]

    if "VARCHAR" in vars(FIELD_TYPE):
        field_types.append(FIELD_TYPE.VARCHAR)

    for field_type in field_types:
        CONVERSIONS[field_type] = [(FLAG.BINARY, str)] + CONVERSIONS[field_type]

    IntegrityError = MySQLdb.IntegrityError
    OperationalError = MySQLdb.OperationalError

