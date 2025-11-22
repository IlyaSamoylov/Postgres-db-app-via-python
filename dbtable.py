# Базовые действия с таблицами

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
        return sorted(self.columns().keys(), key = lambda x: x)

    def primary_key(self):
        return ['id']

    def column_names_without_id(self):
        res = sorted(self.columns().keys(), key = lambda x: x)
        if 'id' in res:
            res.remove('id')
        return res

    def table_constraints(self):
        return []

    def create(self):
        arr = [k + " " + " ".join(v) for k, v in
               sorted(self.columns().items(), key=lambda x: x[0])]

        cols = ", ".join(arr + self.table_constraints())
        # TODO: я не уверен, что параметры self. можно передавать напрямую, потому что они тоже могут задаваться извне через другие функции
        sql = f"CREATE TABLE {self.table_name()} (%s)"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, cols)
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

    # Удаление сущностей нужно обоим таблицам, так что пусть определяется в родительском классе
    def del_entities(self, where_clause):

        # строка не пишет условие where, если where_clause is None, то есть условие не передано
        sql = (f"DELETE FROM {self.table_name()}"
               f"{(where_clause is not None) * "WHERE %(col)s = %(val)s"}"
                )
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, where_clause)
        return cur.fetchall