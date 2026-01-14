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

	if s == '':
		return ''

	return s  # значение или ""

def input_num(prompt, onlyint=False):
	while True:
		raw = input_text(prompt)

		if raw == "quit":
			return "quit"
		if raw == "":
			return ""

		try:
			return int(raw) if onlyint else float(raw)
		except:
			print("Введите число или 'q'.")

def input_yn(prompt, default="y"):
	while True:
		raw = input_text(prompt)

		if raw == "":
			return ''

		if raw in ("y", "n"):
			return raw

		if raw == "quit":
			return 'quit'

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


			col_order = table_obj.column_names_without_id()
			human_headers = [COLUMN_NAMES_MAP.get(c, c) for c in col_order]

			if not rows:
				print("Нет данных.")
				return ctx, rows

			#   используя полный список column_names()
			full_cols = table_obj.column_names()
			row_indexes = [full_cols.index(c) for c in col_order]

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
