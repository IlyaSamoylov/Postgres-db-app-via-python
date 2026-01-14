# Таблица коллекций и особые действия с ней

from ProjectPostgreSQL.dbtable import *

class ExhibitsTable(DbTable):
	def table_name(self):
		return self.dbconn.prefix + "exhibits"

	def columns(self):

		return {"id": ["serial", "PRIMARY KEY"],
				"name": ["varchar(50)", "NOT NULL"],
				"description": ["text"],
				"insurance_value": ["decimal(12,2)", "CHECK(insurance_value >= 0)", "DEFAULT 0"],
				"century": ["smallint", "CHECK (century <= 21)"],
				"collection_id": ["int", "NOT NULL", "REFERENCES Collections(id)", "ON DELETE CASCADE"],
				"hall_id": ["int"],
				"height": ["decimal(6,2)", "CHECK (height > 0)"],
				"width": ["DECIMAL(6, 2)", "CHECK(width > 0)"],
				"length": ["DECIMAL(6, 2)", "CHECK(length > 0)"],
				"need_temp_control": ["CHAR(1)", "NOT NULL",
									  "CHECK(need_temp_control IN('y', 'n'))", "DEFAULT 'y'"],
				"need_humidity_control": ["CHAR(1)", "NOT NULL",
										  "CHECK(need_humidity_control  IN('y', 'n'))", "DEFAULT 'y'"],
				"protected_from_people": ["CHAR(1)", "NOT NULL",
										  "CHECK(protected_from_people IN('y', 'n'))",
										  "DEFAULT 'y'"],
		}

	def not_null_cols(self):
		return ["name", "collection_id", "need_temp_control", "need_humidity_control", "protected_from_people"]

	def default_cols(self):
		return ["insurance_value", "collection_id", "need_temp_control", "need_humidity_control", "protected_from_people"]

	def table_constraints(self):
		return [
			"FOREIGN KEY (collection_id) REFERENCES " +
			self.dbconn.prefix + "collections(id) ON DELETE CASCADE"
		]

	def find_by_position(self, num):
		sql = "SELECT * FROM " + self.table_name()
		sql += " ORDER BY "
		sql += ", ".join(self.primary_key())
		sql += " LIMIT 1 OFFSET %(offset)s"
		cur = self.dbconn.conn.cursor()
		cur.execute(sql, {"offset": num - 1})
		return cur.fetchone()

	def all_by_collection_id(self, col_id):
		sql = "SELECT * FROM " + self.table_name()
		sql += " WHERE collection_id = %s "
		sql += "ORDER BY "
		sql += ", ".join(self.primary_key())
		cur = self.dbconn.conn.cursor()
		cur.execute(sql, str(col_id))
		return cur.fetchall()

	# Удаление сущностей нужно обоим таблицам, так что пусть определяется в родительском классе

	def select_by_col_id(self, collection_id):
		sql = f"SELECT * FROM {self.table_name()} WHERE collection_id = %s"
		cur = self.dbconn.conn.cursor()
		cur.execute(sql, (collection_id,))
		return cur.fetchall()

	def add_by_col_id(self, collection_id, values: dict):

		# Добавляем collection_id
		values["collection_id"] = collection_id

		# Вытаскиваем все колонки (кроме id)
		cols = self.column_names_without_id()

		# Берём значения в правильном порядке
		vals = [values[col] for col in cols]

		# Используем insert_one (который уже безопасный)
		self.insert_one(vals)

	def validate(self, data: dict):
		MAX_NAME = 50
		MAX_DESC = 500

		errors = []

		not_null = set(self.not_null_cols())
		defaults = set(self.default_cols())

		for col, val in data.items():

			# DEFAULT допустим только для колонок с DEFAULT
			if val == "DEFAULT":
				if col not in defaults:
					errors.append(
						f"{col}: значение DEFAULT недоступно (нет DEFAULT в таблице).")
				continue

			# name
			if col == "name":
				if not isinstance(val, str):
					errors.append("name должно быть строкой.")
				else:
					if not val.strip():
						errors.append("Имя экспоната не может быть пустым.")
					if len(val) > MAX_NAME:
						errors.append(f"Слишком длинное имя (> {MAX_NAME}).")

			# description
			elif col == "description":
				if not isinstance(val, str):
					errors.append("description должно быть строкой.")
				else:
					if len(val) > MAX_DESC:
						errors.append(f"Описание слишком длинное (> {MAX_DESC}).")

			# insurance_value
			elif col == "insurance_value":
				if not isinstance(val, (int, float)):
					errors.append("insurance_value должно быть числом.")
				elif val < 0:
					errors.append("insurance_value должно быть >= 0.")
				else:
					s = str(val)
					if "." in s:
						intp, frac = s.split(".")
						if len(frac) > 2:
							errors.append(
								"Страховая стоимость: максимум 2 знака после точки.")
					if len(s.replace(".", "")) > 12:
						errors.append("Слишком много цифр в insurance_value.")

			# century
			elif col == "century":
				if not isinstance(val, int):
					errors.append("century должен быть целым.")
				elif not (-32768 <= val <= 21):
					errors.append("century должен быть в диапазоне -32768..21.")

			# col_id
			elif col == "collection_id":
				if not isinstance(val, int):
					errors.append("collection_id должен быть целым.")
				elif not (0 < val):
					errors.append("collection_id не может быть меньше 0")

			# dimensions (height/width/length)
			elif col in ("height", "width", "length"):
				if not isinstance(val, (int, float)):
					errors.append(f"{col} должно быть числом.")
				elif val <= 0:
					errors.append(f"{col} должно быть > 0.")

			# hall_id
			elif col == "hall_id":
				if not isinstance(val, int):
					errors.append("hall_id должно быть целым числом.")
				elif val <= 0:
					errors.append("hall_id должно быть > 0.")

			# flags
			elif col in ("need_temp_control", "need_humidity_control",
			             "protected_from_people"):
				if val not in ("y", "n"):
					errors.append(f"{col} должно быть 'y' или 'n'.")

			# неизвестная колонка
			else:
				errors.append(f"Неизвестная колонка: {col}")

		for e in errors:
			print(" -", e)
		return errors


