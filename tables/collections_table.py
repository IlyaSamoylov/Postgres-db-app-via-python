# Таблица коллекций и особые действия с ней

from dbtable import *

class CollectionsTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "collections"

    def columns(self):
        return {"id": ["serial", "PRIMARY KEY"],
                "name": ["varchar(50)", "NOT NULL", "UNIQUE"],
                "description": ["text"]}

    def find_by_position(self, num):
        sql = (f"SELECT * FROM {self.table_name()} "
               f"ORDER BY {", ".join(self.primary_key())} "
               f"LIMIT 1 OFFSET {num}")
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()