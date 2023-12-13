from postgredb import PostgreDB
from singleton import Singleton


class DBManager(object, metaclass=Singleton):
    def __init__(self):
        self.db = PostgreDB()
