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
		return list(self.columns().keys())

	def primary_key(self):
		return ['id']

	def column_names_without_id(self):

		res = list(self.columns().keys())
		if 'id' in res:
			res.remove('id')
		return res

	def table_constraints(self):
		return []

	def create(self):

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

	def insert_one(self, data: dict):
		"""
			обычные значения → col = %s
		"""
		if not data:
			print("Нет изменений — обновление не выполнено.")
			return

		# --- Валидация перед выполнением ---
		errors = self.validate(data)
		if errors:
			print("Вставка отменена из-за ошибок.")
			return

		columns = []
		placeholders = []
		values = []

		for col, val in data.items():
			columns.append(col)

			# NULL (без placeholder)
			if val is None:
				placeholders.append("NULL")

			# обычное значение → %s + добавление в values
			else:
				placeholders.append("%s")
				values.append(val)

		sql = f"""
	        INSERT INTO {self.table_name()}
	        ({", ".join(columns)})
	        VALUES ({", ".join(placeholders)})
	    """

		try:
			cur = self.dbconn.conn.cursor()
			cur.execute(sql, values)
			self.dbconn.conn.commit()
		except psycopg2.Error as e:
			self.dbconn.conn.rollback()
			print("Ошибка БД при вставке:")
			print("  SQL:", sql)
			print("  VALUES:", values)
			print("  Ошибка:", e)
			print("Действие отменено")
			return
		print(f"Запись успешно добавлена в {self.table_name()}")

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

		try:
			cur = self.dbconn.conn.cursor()
			cur.execute(sql, params)
			self.dbconn.conn.commit()
		except psycopg2.Error as e:
			self.dbconn.conn.rollback()
			print("Ошибка БД при удалении:")
			print("  SQL:", sql)
			print("  VALUES:", params)
			print("  Ошибка:", e)
			print("Действие отменено")
			return

	def update_ents(self, where: tuple, data: dict):
		"""
		UPDATE с поддержкой:
			обычные значения → col = %s
		"""
		# если изменений нет
		if not data:
			print("Нет изменений — обновление не выполнено.")
			return

		errors = self.validate(data)
		if errors:
			print("Обновление отменено из-за ошибок.")
			return

		sets = []
		values = []

		for col, val in data.items():
			sets.append(f"{col}=%s")
			values.append(val)

		# Защита от пустого SET (на всякий случай)
		if not sets:
			print("Нет полей для обновления.")
			return

		# where — это tuple вида ("id", 5)
		where_col, where_val = where

		sql = f"""
	        UPDATE {self.table_name()}
	        SET {", ".join(sets)}
	        WHERE {where_col} = %s
	    """
		values.append(where_val)

		try:
			cur = self.dbconn.conn.cursor()
			cur.execute(sql, values)
			self.dbconn.conn.commit()
		except psycopg2.Error as e:
			self.dbconn.conn.rollback()
			print("Ошибка БД при обновлении:")
			print("  SQL:", sql)
			print("  VALUES:", values)
			print("  Ошибка:", e)
			print("Действие отменено")
			return



