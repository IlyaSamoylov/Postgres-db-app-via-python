# Валидация

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

		if s == "1":
			return None
		try:
			v = float(s)
			if onlyint:
				v = int(s)
		except ValueError:
			print("Невалидное число. Повторите ввод (или 1 для отмены).")
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

