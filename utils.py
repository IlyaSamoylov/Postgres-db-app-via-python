# TODO: Спросить, как добавить в проект prettytable, чтобы у преподавателя тоже добавился
# Валидация
# TODO" Наверное стоит настроить отмены на какие-то значения, которые редко вписсывают,
#  например None, все равно вместо им можно заполнять, если нажмут enter
# def input_opt(prompt, nonempty=False):
# 	"""
# 	Проверяет:
# 		- нажал ли пользователь 1 (отмена)
# 		- ввел ли пользователь пустую строку, если она запрещена (nonempty = True)
#
# 	Возвращает:
# 		- None, если введена отмена
# 		- Значение либо пусто, если nonempty = False
# 	"""
# 	while True:
# 		s = input(prompt).strip()
#
# 		if s == "1":
# 			return None
# 		if nonempty and len(s) == 0:
# 			print("Поле не может быть пустым. Введите заново (или 1 для отмены).")
# 			continue
# 		return s

def input_text(prompt: str):
	"""
	Возвращает:
		"quit"   → отмена
		""       → пропуск (skip) в update
		строку   → текст
		"/"      -> оставить старое значение (для update)
	"""
	s = input(prompt).strip()

	if s == "q":
		return "quit"
	# if s.lower().strip() in ("default", ""):
	# 	return "DEFAULT"  # DEFAULT keyword
	if s == '':
		return ''
	# if s == "/":
	# 	return "/old"
	return s  # значение или ""

#
# def val_input_num(prompt, onlyint=False):
# 	"""
# 	Проверяет, ввел ли пользователь целое число.
# 	Если isfloat = True, то оно может быть float
# 	"""
# 	while True:
# 		s = input(prompt).strip()
#
# 		if s == "0":
# 			return None
# 		try:
# 			v = float(s)
# 			if onlyint:
# 				v = int(s)
# 		except ValueError:
# 			print("Невалидное число. Повторите ввод (или 0 для отмены).")
# 			continue
# 		return v


def input_num(prompt, onlyint=False):
	while True:
		raw = input_text(prompt)

		if raw == "quit":
			return "quit"
		if raw == "":
			return ""

		# if raw in ("quit", None, "DEFAULT"):
		# 	return raw
		# if raw == "":
		# 	return "DEFAULT"
		# if raw == "/":
		# 	return "/old"

		try:
			return int(raw) if onlyint else float(raw)
		except:
			print("Введите число или 'q'.")



# def input_char_yn(prompt, default="y"):
# 	while True:
# 		s = input(prompt + f" (y/n, ENTER для {default}):").strip()
#
# 		if s == "":
# 			return default
# 		if s not in ("y", "n"):
# 			print("Введите 'y' или 'n'.")
# 			continue
# 		return s

# def input_yn(prompt: str, default="y"):
# 	while True:
# 		s = input_text(prompt + f" (y/n, ENTER={default}): ")
#
# 		if s in ("quit", ""):
# 			return s
#
# 		if s is None:
# 			return None
#
# 		if s.lower() in ("y", "n"):
# 			return s.lower()
#
# 		print("Введите y или n.")

def input_yn(prompt, default="y"):
	while True:
		raw = input_text(prompt)

		if raw == "":
			return ''

		if raw in ("y", "n"):
			return raw

		print("Введите y/n или 'q'.")


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

				print("\n< - назад, > - вперёд, 0 - действия")
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
