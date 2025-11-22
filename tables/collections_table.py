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
        set_dict: dict(col:val) - колонки и значения для set,
        например {"name": "New Name", "description": "New Text"}
        """

        set_part = ", ".join(f"{col} = %s" for col in set_dict.keys())
        where_col, where_val = where_clause

        sql = f"UPDATE {self.table_name()} SET {set_part} WHERE {where_col} = %s"

        params = list(set_dict.values()) + [where_val]

        cur = self.dbconn.conn.cursor()
        cur.execute(sql, params)
        self.dbconn.conn.commit()
