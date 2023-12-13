from contextlib import closing
from typing import Dict

import psycopg2
from PyQt5.QtCore import QThread
from psycopg2._psycopg import connection

from dbconfig import conn_params, create_table_queries


class PostgreDB():
    def __init__(self):
        self.dc_connection: Dict[QThread, connection] = {}
        self.create_tables()
        pass

    def get_connection(self) -> connection:
        thread = QThread.currentThread()
        if thread not in self.dc_connection:
            conn = None
            try:
                conn = psycopg2.connect(**conn_params)
            except Exception as e:
                print(e.__traceback__)

            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

            self.dc_connection[thread] = conn
        return self.dc_connection[thread]

    def execute_cud(self, query):
        try:
            with closing(self.get_connection().cursor()) as cursor:
                cursor.execute(query)
                cursor.commit()
        except Exception as e:
            print(e.__traceback__)

    def execute_read_one(self, query):
        try:
            with closing(self.get_connection().cursor()) as cursor:
                cursor.execute(query)
                records = cursor.fetchone()
                return records
        except(Exception, psycopg2.DatabaseError) as e:
            print("Error while retrieving values {}".format(e))

    def execute_read_all(self, query):
        try:
            with closing(self.get_connection().cursor()) as cursor:
                cursor.execute(query)
                records = cursor.fetchall()
                return records
        except(Exception, psycopg2.DatabaseError) as e:
            print("Error while retrieving values {}".format(e))

    def create_tables(self):
        conn = cursor = None

        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # 각 테이블 생성 쿼리 실행
            for query in create_table_queries:
                cursor.execute(query)
            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                cursor.close()
                conn.close()
