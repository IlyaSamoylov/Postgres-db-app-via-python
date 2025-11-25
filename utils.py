# TODO: Спросить, как добавить в проект prettytable, чтобы у преподавателя тоже добавился
# Валидация
# TODO" Наверное стоит настроить отмены на какие-то значения, которые редко вписсывают,
#  например None, все равно вместо им можно заполнять, если нажмут enter
def input_opt(prompt, nonempty=False):
	"""
	Проверяет:
		- нажал ли пользователь 1 (отмена)
		- ввел ли пользователь пустую строку, если она запрещена (nonempty = True)

	Возвращает:
		- None, если введена отмена
		- Значение либо пусто, если nonempty = False
	"""
	while True:
		s = input(prompt).strip()

		if s == "1":
			return None
		if nonempty and len(s) == 0:
			print("Поле не может быть пустым. Введите заново (или 1 для отмены).")
			continue
		return s

def val_input_num(prompt, onlyint=False):
	"""
	Проверяет, ввел ли пользователь целое число.
	Если isfloat = True, то оно может быть float
	"""
	while True:
		s = input(prompt).strip()

		if s == "0":
			return None
		try:
			v = float(s)
			if onlyint:
				v = int(s)
		except ValueError:
			print("Невалидное число. Повторите ввод (или 0 для отмены).")
			continue
		return v

def input_char_yn(prompt, default="y"):
	while True:
		s = input(prompt + f" (y/n, ENTER для {default}):").strip()

		if s == "":
			return default
		if s not in ("y", "n"):
			print("Введите 'y' или 'n'.")
			continue
		return s

COLUMN_NAMES_MAP = {
	"id": "№",
	"name": "Название",
	"description": "Описание",
	"insurance_value": "Страховая стоимость",
	"century": "Век",
	"collection_id": "Коллекция",
	"hall_id": "Зал",
	"height": "Высота (см)",
	"width": "Ширина (см)",
	"length": "Длина (см)",
	"need_temp_control": "Темп. контроль",
	"need_humidity_control": "Контроль влажности",
	"protected_from_people": "Защита"
}

def build_readable_columns(table_obj):
	"""Преобразует таблицу.columns() в читаемый список заголовков."""
	col_names = table_obj.column_names()     # ['id','name','description']
	readable = [COLUMN_NAMES_MAP.get(col, col) for col in col_names]
	return col_names, readable


# def table_paginator(page_size=5):
# 	"""
# 	Декоратор для показа таблицы постранично.
# 	Декорируемая функция должна вернуть:
# 		(table_obj, columns_dict, rows)  или
# 		(table_obj, columns_dict, rows, ctx)
# 	- table_obj: экземпляр таблицы (например CollectionsTable())
# 	- columns_dict: результат table_obj.columns()
# 	- rows: список кортежей (cur.fetchall())
# 	- ctx: дополнительный контекст (например coll_id), опционально
# 	Декоратор печатает страницы и возвращает (ctx, rows) по завершении просмотра,
# 	чтобы меню могло использовать уже выбранную коллекцию/строки
# 	(вместо повторного запроса выбора).
# 	"""
# 	def decorator(func):
# 		def wrapper(self, *args, **kwargs):
# 			# вызвать функцию-источник данных
# 			res = func(self, *args, **kwargs)
# 			# разрешаем, чтобы функция вернула None (например отмена выбора)
# 			if not res:
# 				# возвращаем (None, []) — чтобы caller знал, что нет контекста/строк
# 				return None, []
#
# 			# Поддерживаем два формата возврата: 3 или 4 элементов
# 			if len(res) == 3:
# 				table_obj, columns_dict, rows = res
# 				ctx = None
# 			elif len(res) == 4:
# 				table_obj, columns_dict, rows, ctx = res
# 			else:
# 				raise ValueError("table_paginator: функция должна возвращать (table, columns, rows) или (table, columns, rows, ctx)")
#
# 			# Если колонок нет или table_obj не передан — пустой результат
# 			if not columns_dict or table_obj is None:
# 				print("Нет данных (структура таблицы не определена).")
# 				return ctx, rows
#
# 			col_order = table_obj.column_names()  # порядок колонок соответствует column_names()
# 			human_headers = [COLUMN_NAMES_MAP.get(c, c) for c in col_order]
#
# 			# Если строк нет — даём возможность меню работать (возвращаем ctx,rows)
# 			if not rows:
# 				print("Нет данных.")
# 				return ctx, rows
#
# 			total = len(rows)
# 			page = 1
# 			while True:
# 				start = (page - 1) * page_size
# 				end = start + page_size
# 				page_items = rows[start:end]
#
# 				print("\n" + "-"*60)
# 				print(f"Страница {page} / { (total + page_size - 1)//page_size }")
# 				print("-"*60)
# 				# заголовки
# 				print("\t".join(human_headers))
# 				# строки
# 				for i, row in enumerate(page_items, start=1):
# 					# строим строку в порядке col_order, используя column_names() индексы
# 					values = []
# 					for c in col_order:
# 						idx = table_obj.column_names().index(c)
# 						val = row[idx] if idx < len(row) else ""
# 						values.append(str(val) if val is not None else "")
# 					print("\t".join(values))
#
# 				# навигация
# 				print("\n< - назад, > - вперёд, 0 - выход (вернуться в меню)")
# 				cmd = input("=> ").strip()
# 				if cmd == "<" and page > 1:
# 					page -= 1
# 				elif cmd == ">" and end < total:
# 					page += 1
# 				elif cmd == "0":
# 					# возвращаем контекст и текущие rows для after_*
# 					return ctx, rows
# 				else:
# 					print("Неизвестная команда.")
# 		return wrapper
# 	return decorator

# TODO: Вместо номеров пишутся id - нехорошо. Как сопоставить номер строки на экране и id?
# Новый вариант: перед каждой строкой выводится нормальный порядковый номер,
# а не id из таблицы.

def table_paginator(page_size=5):

	def decorator(func):
		def wrapper(self, *args, **kwargs):
			res = func(self, *args, **kwargs)
			if not res:
				return None, []

			# Распаковка результатов
			if len(res) == 3:
				table_obj, columns_dict, rows = res
				ctx = None
			elif len(res) == 4:
				table_obj, columns_dict, rows, ctx = res
			else:
				raise ValueError("table_paginator: ожидается (table, columns, rows) или (table, columns, rows, ctx)")

			if not columns_dict or table_obj is None:
				print("Нет данных (структура таблицы не определена).")
				return ctx, rows

			# ✔ правильно: берём колонки БЕЗ id
			col_order = table_obj.column_names_without_id()
			human_headers = [COLUMN_NAMES_MAP.get(c, c) for c in col_order]

			if not rows:
				print("Нет данных.")
				return ctx, rows

			# ✔ правильно: ищем ИНДЕКСЫ этих колонок внутри row,
			#   используя полный список column_names()
			full_cols = table_obj.column_names()
			row_indexes = [full_cols.index(c) for c in col_order]

			# ✔ вычисляем ширины колонок
			col_widths = []
			for idx, h in zip(row_indexes, human_headers):
				max_content_width = max([len(str(row[idx])) for row in rows] + [len(h)])
				col_widths.append(min(max_content_width, 50))

			total = len(rows)
			page = 1

			while True:
				start = (page - 1) * page_size
				end = start + page_size
				page_items = rows[start:end]

				print("\n" + "-" * 80)
				print(f"Страница {page} / { (total + page_size - 1) // page_size }")
				print("-" * 80)

				# Заголовок
				header_line = f"{'№':<4} | " + " | ".join(
					f"{h:<{w}}" for h, w in zip(human_headers, col_widths)
				)
				print(header_line)
				print("-" * len(header_line))

				# ✔ печать строк без id
				for i, row in enumerate(page_items, start=start + 1):
					row_line = [f"{i:<4}"]  # порядковый номер
					for idx, w in zip(row_indexes, col_widths):
						val = row[idx]
						val_str = str(val) if val is not None else ""
						if len(val_str) > w:
							val_str = val_str[:w - 3] + "..."
						row_line.append(f"{val_str:<{w}}")
					print(" | ".join(row_line))

				print("\n< - назад, > - вперёд, 0 - выход")
				cmd = input("=> ").strip()

				if cmd == "<" and page > 1:
					page -= 1
				elif cmd == ">" and end < total:
					page += 1
				elif cmd == "0":
					return ctx, rows
				else:
					print("Неизвестная команда.")

		return wrapper
	return decorator
