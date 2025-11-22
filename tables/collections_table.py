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
               f"LIMIT 1 OFFSET  %(offset)s")
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": num - 1})
        return cur.fetchone()

    # TODO: для таблицы Collections доработать функции удаления и редактирования сущностей.
    #  Интерфейс не должен работать с id!

    # TODO: можно попробовать учесть все (, ), AND, OR, BETWEEN, IN, etc
    # Удаление сущностей нужно обоим таблицам, так что пусть определяется в родительском классе

    def update_ents(self, where_clause, set_dict):
        """
        where_clause: (col, val) - условие и значение для where
        set_dict: dict(col:val) - колонки и значения для set
        """
        fullset = ", ".join(["SET " + k + " = " + v for k, v in set_dict.items()])
        sql = f"UPDATE {self.table_name()} %(fullset)s  WHERE %(condw)s = %(valw)s"
        cur = self.dbconn.conncursor()
        cur.execute(sql, {"fullset": fullset, "cond_w": where_clause[0], "valw": where_clause[1]})
        return cur.fetchall