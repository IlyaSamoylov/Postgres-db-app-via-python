# Базовые действия с таблицами
# TODO: Сделано или все таки пока нет:
#  доработав все проверки целостности данных и соответствия типам данных (не должно при
#  добавлении, и других действиях происходить ошибок PostgreSQL, приводящих к «вылету» программы
#  или действиям программы, не имеющим нормальных объяснений).
from dbconnection import *

class DbTable:
    dbconn = None

    def __init__(self):
        return

    def table_name(self):
        return f"{self.dbconn.prefix} table"

    def columns(self):
        return {"test": ["integer", "PRIMARY KEY"]}

    def column_names(self):
        # Снова, зачем?
        # return sorted(self.columns().keys(), key = lambda x: x)
        return list(self.columns().keys())

    def primary_key(self):
        return ['id']

    def column_names_without_id(self):
        # Зачем была эта сортировка колонок таблицы?!
        # res = sorted(self.columns().keys(), key = lambda x: x)
        res = list(self.columns().keys())
        if 'id' in res:
            res.remove('id')
        return res

    def table_constraints(self):
        return []

    def create(self):
        # Зачем сортировка колонок бл*ть?!
        # arr = [k + " " + " ".join(v) for k, v in
        #        sorted(self.columns().items(), key=lambda x: x[0])]
        arr = [k + " " + " ".join(v) for k, v in list(self.columns().items())]

        cols = ", ".join(arr + self.table_constraints())

        sql = f"CREATE TABLE {self.table_name()} ({cols})"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def drop(self):
        sql = f"DROP TABLE IF EXISTS {self.table_name()}"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def insert_one(self, vals):
        # for i in range(0, len(vals)):
        #     if type(vals[i]) == str:
        #         vals[i] = "'" + vals[i] + "'"
        #     else:
        #         vals[i] = str(vals[i])

        cols = ", ".join(self.column_names_without_id())
        placeholders = ", ".join(["%s"] * len(vals))
        sql = f"INSERT INTO {self.table_name()} ({cols}) VALUES ({placeholders})"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, tuple(vals))

        self.dbconn.conn.commit()
        return

    def first(self):
        prim_k = ", ".join(self.primary_key())
        sql = f"SELECT * FROM {self.table_name()} ORDER BY {prim_k}"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()        

    def last(self):
        desc_primk = ", ".join([x + " DESC" for x in self.primary_key()])
        sql = f"SELECT * FROM {self.table_name()} ORDER BY {desc_primk}"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def all(self):
        order_by = ", ".join(self.primary_key())
        sql = f"SELECT * FROM {self.table_name()} ORDER BY {order_by}"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def del_entities(self, where_clause=None):
        """
        where_clause: tuple(str, any)
            (column_name, column_value)
            пример: ("name", "Old Name")
        """
        sql = f"DELETE FROM {self.table_name()}"
        params = ()

        if where_clause is not None:
            col, val = where_clause
            sql += f" WHERE {col} = %s"
            params = (val,)

        cur = self.dbconn.conn.cursor()
        cur.execute(sql, params)
        self.dbconn.conn.commit()

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

