# Таблица коллекций и особые действия с ней

from dbtable import *

class ExhibitsTable(DbTable):
	def table_name(self):
		return self.dbconn.prefix + "exhibits"

	def columns(self):
		# можно ли здесь оставить CHECK/DEFAULT
		return {"id": ["serial", "PRIMARY KEY"],
				"name": ["varchar(50)", "NOT NULL"],
				"description": ["text"],
				"insurance_value": ["decimal(12,2)", "CHECK(insurance_value >= 0", "DEFAULT 0"],
				"century": ["smallint", "CHECK (century <= 21)"],
				"collection_id": ["int", "NOT NULL", "REFERENCES Collection(id)", "ON DELETE CASCADE"],
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
		sql += " WHERE collection_id = %s"
		sql += "ORDER BY "
		sql += ", ".join(self.primary_key())
		cur = self.dbconn.conn.cursor()
		cur.execute(sql, str(col_id))
		return cur.fetchall()

	# TODO: для таблицы Exhibits доработать функции просмотр списка сущностей по
	#  указанному значению ключа из первой таблицы, добавление новых сущностей с этим ключом
	#  (включая все проверки целостности данных и соответствия типам данных), удаление сущностей
	#  в этом же интерфейсе. Без суррогатных ключей, только нетехнические записи и номер на экране
	# Удаление сущностей нужно обоим таблицам, так что пусть определяется в родительском классе

	def select_by_col_id(self, target_id):
		sql = f"SELECT * FROM {self.table_name()} WHERE collection_id = %s"
		cur = self.dbconn.conn.cursor()
		cur.execute(sql, target_id)
		return cur.fetchall

	def add_by_col_id(self, target_id, values):
		self.insert_one(1)
		pass
	

