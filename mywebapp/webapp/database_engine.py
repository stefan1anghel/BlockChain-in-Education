import pyodbc
from .Utils.singleton import Singleton


@Singleton
class DbEngine:
    def __init__(self):
        self.db = None
        self.is_connected = False

    def _connect(self):
        self.db = pyodbc.connect(
            'DRIVER={SQL Server};'
            'Server=DESKTOP-7SKBPIV\\SQLEXPRESS;'
            'Database=Proiect_Licenta;'
            'Trusted_Connection=yes;'
        )
        self.is_connected = True

    def _disconnect(self):
        if self.is_connected is True:
            self.db.cursor().close()
            self.is_connected = False

    def run_query(self, query_string):
        is_select = False
        if query_string.split(" ")[0] == "select":
            is_select = True
        new_output = []
        self._connect()
        with self.db.cursor() as conn:
            conn.execute(query_string)
            if is_select:
                for entry in conn:
                    new_output.append(entry)
                self._disconnect()
                return new_output
        self._disconnect()
