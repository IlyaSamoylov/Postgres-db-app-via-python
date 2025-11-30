# Таблица коллекций и особые действия с ней
# TODO: Отлов неправильного ввода через try...except
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

    # NOT NULL колонки
    def not_null_cols(self):
        return ["name"]

    def default_cols(self):
        return []

    def validate(self, data: dict):
        MAX_NAME = 50
        MAX_DESC = 2000
        errors = []

        not_null = set(self.not_null_cols())
        defaults = set(self.default_cols())

        for col, val in data.items():

            # DEFAULT: допускаем только если у колонки реально есть DEFAULT
            if val == "DEFAULT":
                if col not in defaults:
                    errors.append(
                        f"{col}: значение DEFAULT недоступно (нет DEFAULT в таблице).")
                continue

            # NULL
            if val is None:
                if col in not_null:
                    errors.append(f"{col} не может быть NULL.")
                continue

            # Пустые строки допускаем только для description
            if col == "name":
                if not isinstance(val, str):
                    errors.append("name должно быть строкой.")
                else:
                    if not val.strip():
                        errors.append("Название не может быть пустым.")
                    if len(val) > MAX_NAME:
                        errors.append(f"Название слишком длинное (> {MAX_NAME}).")

            elif col == "description":
                if not isinstance(val, str):
                    errors.append("description должно быть строкой.")
                else:
                    if len(val) > MAX_DESC:
                        errors.append(f"Описание слишком длинное (> {MAX_DESC}).")

        # вывод ошибок
        for e in errors:
            print(" -", e)
        return errors

    # TODO: для таблицы Collections доработать функции удаления и редактирования сущностей.
    #  Интерфейс не должен работать с id!

    # Удаление сущностей нужно обоим таблицам, так что пусть определяется в родительском классе

