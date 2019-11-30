from __future__ import absolute_import, division, with_statement

import copy
import itertools
import os
import logging
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


class Connection(object):
    def __init__(self, host, database, user=None, password=None,
                 max_idel_time=7 * 3600, connect_timeout=0, time_zone="+0:00",
                 charset="utf-8", sql_mode="TRADITIONAL"):
        self.host = host
        self.database = database
        self.max_idel_time = float(max_idel_time)

        args = dict(conv=CONVERSIONS, use_unicode=True, charset=charset,
                    db=database, init_command=("SET time_zone='%s'"%time_zone),
                   connect_timeout=connect_timeout, sql_mode=sql_mode)

        if user is not None:
            args["user"] = user
        if password is not None:
            args["passwd"] = password

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
            logging.error("Cannot connect to MySQL on %s", self.host,
                          exc_info=True)
    def __del__(self):
        self.close()

    def reconnect(self):
        self.close()
        self._db = MySQLdb.connect(**self._db_args)
        self._db.autocommit(True)

    def close(self):
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def iter(self, query, *parameters, **kwparameters):
        self._ensure_connected()
        cursor = MySQLdb.cursors.SSCursor(self._db)
        try:
            self._execute(cursor, query, parameters, kwparameters)
            columns_names = [d[0] for d in cursor.description]
            for row in cursor:
                yield Row(zip(columns_names, row))
        finally:
            cursor.close()

    def query(self, query, *parameters, **kwparameters):
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            columns_names = [d[0] for d in cursor.description]
            return [Row(itertools.zip(columns_names, row)) for row in in cursor]
        finally:
            cursor.close()

    def get(self, query, *parameters, **kwparameters):
        rows = self.query(query, *parameters, **kwparameters)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            retur rows[0]

    def execute(self, query, *parameters, **kwparameters):
        return self.execute_lastrowid(query, *parameters, **kwparameters)

    def execute_lastrowid(self, query, *parameters, **kwparameters):
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def execute_rowcount(self, query, *parameters, **kwparameters):
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def executemany(self, query, parameters):
        return self.executemany_lastrowid(query, parameters)

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
    updatemany = executemany_rowcount

    insert = execute_lastrowid
    insertmany = executemany_lastrowid

    def _ensure_connected(self):
        if (self._db is None or (time.time() - self._last_use_time >
                                 self.max_idel_time)):
            self.reconnect()
        self._last_use_time = time.time()

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()

    def _execute(self, cursor, query, parameters, kwparameters):
        try:
            return cursor.execute(query, kwparameters, or parameters)
        except OperationalError:
            logging.error("Error connection to MySQL on %s", self.host)
            self.close()
            raise


class Row(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


if MySQLdb is not None:
    FIELD_TYPE = MySQLdb.constants.FIELD_TYPE
    FLAG = MySQLdb.constants.FLAG
    CONVERSIONS = copy.copy(MySQLdb.converters.conversions)

    field_types = [FIELD_TYPE.BLOB, FIELD_TYPE.STRING, FIELD_TYPE.VAR_STRING]
    if "VARCHAR" in vars(FIELD_TYPE):
        field_types.append(FIELD_TYPE.VARCHAR)

    for field_type in field_types:
        CONVERSIONS[field_type] = [(FLAG.BINARY, str)] + CONVERSIONS[field_type]

    IntegrityError = MySQLdb.IntegrityError
    OperationalError = MySQLdb.OperationalError

