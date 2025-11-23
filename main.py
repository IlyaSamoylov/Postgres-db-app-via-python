# TODO: Сравнить с эталонным main и узнать, не слишком ли сильно изменена изначальная логика. В идеале все же придерживаться изначального сценария
import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *
from tables.collections_table import *
from tables.exhibits_table import *
from utils import *

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        colt = CollectionsTable()
        ext = ExhibitsTable()
        colt.create()
        ext.create()
        return

    def db_insert_somethings(self):
        colt = CollectionsTable()
        ext = ExhibitsTable()

        #  Не забыть, что надо также проверять валидность данных
        colt.insert_one(["Челябинский метеорит и космо‑наследие", "Коллекция, посвящённая знаменитому челябинскому метеориту — его фрагменты, история падения и исследования."])
        colt.insert_one(["История быта и культуры Южного Урала", "Экспозиция, отражающая народный быт, этнографию и культуру населения края."])
        colt.insert_one(["XX век: индустриализация и война", "Коллекция, посвящённая истории Урала в XX веке: промышленность, война, советский период."])
        ext.insert_one(["Фрагмент метеорита Чебаркуль", "Кусок метеорита, найденного в Челябинской области после падения в озеро Чебаркуль.", 1000000.00, 21, 1, 5, 50.00, 40.00, 25.00, 'n', 'n', 'y'])
        ext.insert_one(["Керамический горшок XIX века", "Глиняный горшок из крестьянского быта Южного Урала.", 5000.00, 19, 2, 2, 30.00, 30.00, 30.00, 'n', 'n', 'y'])
        ext.insert_one(["Плакат индустриализации Урала", "Плакат советского периода, демонстрирующий развитие промышленности.", 12000.00, 20, 3, 3, 80.00, 60.00, 1.00, 'n', 'n', 'y'])

    def db_drop(self):
        colt = CollectionsTable()
        ext = ExhibitsTable()
        colt.drop()
        ext.drop()
        return

    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр коллекций;
    2 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step

    def print_menu(self, menu):
        for k, v in menu.items():
            print(k, v)

    # Collections UI ===================
    @table_paginator(page_size=5)
    def show_collections(self):
        table = CollectionsTable()
        return table, table.columns(), table.all()

    def after_show_collections(self, cmd):
        menu = {
            "3": "Добавить коллекцию",
            "4": "Удалить коллекцию",
            "5": "Просмотр экспонатов коллекции",
            "6": "Редактировать коллекцию",
            "0": "Возврат в главное меню",
            "9": "Выход"
        }

        if cmd not in menu:
            print("Неизвестная команда.")
            return "1"

        if cmd == "3":
            self.add_collection()
            return "1"

        if cmd == "4":
            self.delete_collection()
            return "1"

        if cmd == "5":
            # сначала показать экспонаты
            coll_ctx, rows = self.show_exhibits_by_collection()
            # затем меню экспонатов
            return self.after_show_exhibits(coll_ctx, rows)

        if cmd == "6":
            self.edit_collection()
            return "1"

        # возврат напрямую
        return cmd

    def after_show_exhibits(self, coll_id=None, rows=None):
        menu = {
            "6": "- Добавить экспонат",
            "7": "- Удалить экспонат",
            "8": "- Редактировать экспонат",
            "1": "- Назад к коллекциям",
            "0": "- Главное меню",
            "9": "- Выход"
        }

        for k, v in menu.items():
            print(f"{k} {v}")

        # Если coll_id уже известен — используем его; иначе предложим выбрать
        if coll_id is None:
            coll = self.choose_collection_by_row()
            if coll is None:
                return "1"  # вернёмся к просмотру коллекций
            coll_id = coll[0]

        # Если rows не переданы, загрузим их
        if rows is None:
            rows = ExhibitsTable().select_by_col_id(coll_id)

        while True:
            cmd = self.read_next_step()

            if cmd == "6":
                # Добавить экспонат в известную коллекцию
                self.add_exhibit_to_collection(coll_id)
                # после добавления остаёмся в том же меню (показать заново)
                return "5"

            if cmd == "7":
                # Удалить — используем переданные rows (или вновь загружаем)
                if not rows:
                    rows = ExhibitsTable().select_by_col_id(coll_id)
                self.delete_exhibit_from_list(rows)
                return "5"

            if cmd == "8":
                if not rows:
                    rows = ExhibitsTable().select_by_col_id(coll_id)
                self.edit_exhibit_in_list(rows)
                return "5"

            if cmd in ("1", "0", "9"):
                return cmd

            print("Неизвестная команда.")

    def add_collection(self):
        print("Добавление коллекции (1 - отмена в любое время)")
        name = input_opt("Введите название: ", nonempty=True)
        if name is None:
            return
        description = input_opt("Введите описание (ENTER для пустого, 1 - отмена): ")
        if description is None:
            return
        CollectionsTable().insert_one([name, description])
        print("Коллекция добавлена.")

    def choose_collection_by_row(self):
        lst = CollectionsTable().all()
        if not lst:
            print("Список коллекций пуст.")
            return None
        while True:
            num = val_input_num("Укажите номер строки коллекции (0 - отмена): ", onlyint=True)
            if num == 0:
                return None
            if num is None or num < 1 or num > len(lst):
                print("Неверный номер. Повторите ввод.")
                continue
            return CollectionsTable().find_by_position(int(num))

    def delete_collection(self):
        coll = self.choose_collection_by_row()
        if coll is None:
            return
        coll_id = coll[0]
        # confirm
        ok = input(
            f"Подтвердите удаление коллекции '{coll[1]}' (y/N): ").strip().lower()
        if ok != "y":
            print("Отмена удаления.")
            return
        CollectionsTable().del_entities(("id", coll_id))
        print("Коллекция удалена (и её экспонаты, если были).")

    def edit_collection(self):
        coll = self.choose_collection_by_row()
        if coll is None:
            return
        coll_id = coll[0]
        print(f"Редактирование коллекции: {coll[1]}")
        new_name = input_opt(f"Новое название (ENTER оставить '{coll[1]}', 1 - отмена): ", nonempty=True)
        if new_name is None:
            return
        if new_name == "":
            new_name = coll[1]
        new_desc = input_opt("Новое описание (ENTER оставить текущим, 1 - отмена): ")
        if new_desc is None:
            return
        if new_desc == "":
            new_desc = coll[2]
        CollectionsTable().update_ents(("id", coll_id),
                                       {"name": new_name, "description": new_desc})
        print("Коллекция обновлена.")

    def show_add_collection(self):
        # Не реализована проверка на максимальную длину строк. Нужно доделать самостоятельно!
        name = input_opt("Введите название коллекции (1 - отмена): ", True)
        if name is None:
            return

        desc = input_opt("Введите описание (ENTER для пустого, 1 - отмена): ")
        if desc is None:
            return
        CollectionsTable().insert_one([name, desc])
        print("Коллекция успешно добавлена")
        return

    #  Exhibits UI ===================
    @table_paginator(page_size=5)
    def show_exhibits_by_collection(self):
        coll = self.choose_collection_by_row()
        if coll is None:
            return None
        coll_id = coll[0]

        table = ExhibitsTable()
        rows = table.select_by_col_id(coll_id)

        return table, table.columns(), rows, coll_id


    def add_exhibit_to_collection(self, coll_id):
        print("Добавление экспоната (1 - отмена)")
        name = input_opt("Название: ", nonempty=True)
        if name is None:
            return
        description = input_opt("Описание (ENTER для пустого): ")
        if description is None:
            return
        insurance_value = val_input_num("Страховая стоимость (число): ")
        if insurance_value is None:
            return
        century = val_input_num("Век (0..21): ", onlyint=True)
        if century is None:
            return
        hall_id = None
        hall_input = val_input_num("Номер зала (целое, ENTER пусто): ", onlyint=True)
        if hall_input is not None and hall_input != "":
            try:
                hall_id = int(hall_input)
            except ValueError:
                print("Значение зала должно быть целым. Отмена")
                return
        height = val_input_num("Высота (см, >0): ")
        # TODO: Наверное, лучше все так вернуть allow_zero
        if height is None or height <= 0:
            return
        width = val_input_num("Ширина (см, >0): ")
        if width is None or width < 0:
            return
        length = val_input_num("Длина (см, >0): ")
        if length is None:
            return
        need_temp = input_char_yn("Требуется контроль температуры?", default="y")
        need_hum = input_char_yn("Требуется контроль влажности?", default="y")
        protected = input_char_yn("Защищено ли от людей?", default="y")

        values = {
            "name": name,
            "description": description,
            "insurance_value": insurance_value,
            "century": century,
            "collection_id": coll_id,
            "hall_id": hall_id,
            "height": height,
            "width": width,
            "length": length,
            "need_temp_control": need_temp,
            "need_humidity_control": need_hum,
            "protected_from_people": protected,
        }

        ExhibitsTable().add_by_col_id(coll_id, values)
        print("Экспонат добавлен.")

    def delete_exhibit_from_list(self, lst):
        if not lst:
            print("Нет экспонатов для удаления.")
            return
        while True:
            num = val_input_num("Номер строки экспоната для удаления (0 - отмена): ", onlyint=True )
            if num == "0":
                return
            if num is None or num < 1 or num > len(lst):
                print("Неверный номер.")
                continue
            row = lst[int(num) - 1]
            ex_id = row[0]
            ok = input(f"Подтвердите удаление '{row[1]}' (y/N): ").strip().lower()
            if ok != "y":
                print("Отмена")
                return
            ExhibitsTable().del_entities(("id", ex_id))
            print("Экспонат удалён.")
            return

    def edit_exhibit_in_list(self, lst):
        if not lst:
            print("Нет экспонатов для редактирования.")
            return
        while True:
            num = val_input_num(
                "Номер строки экспоната для редактирования (0 - отмена): ", onlyint=True)
            if num == "0":
                return
            if num is None or num < 1 or num > len(lst):
                print("Неверный номер.")
                continue
            row = lst[int(num) - 1]
            ex_id = row[0]
            print(f"Редактирование экспоната: {row[1]}")
            new_name = input_opt(
                f"Новое название (ENTER оставить '{row[1]}', 1 - отмена): ", nonempty=True)
            if new_name is None:
                return
            if new_name == "":
                new_name = row[1]
            new_desc = input_opt("Новое описание (ENTER оставить текущим): ")
            if new_desc is None:
                return
            if new_desc == "":
                new_desc = row[2]
            # Для краткости редактируем только name и description; остальные поля можно добавить по аналогии
            ExhibitsTable().update_ents(("id", ex_id),
                                        {"name": new_name, "description": new_desc})
            print("Экспонат обновлён.")
            return

    # MAIN cycle
    def main_cycle(self):
        current_menu = "0"
        next_step = None    # Не используется, но для чего-то должен быть нужен
        while current_menu != "9":
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_collections()
                next_step = self.read_next_step()
                current_menu = self.after_show_collections(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.show_add_collection()
                current_menu = "1"
        print("До свидания!")    
        return

    def test(self):
        DbTable.dbconn.test()

m = Main()
# Откоментируйте эту строку и закоментируйте следующую для теста
# соединения с БД
res = m.connection.test()
print(f"Подключилось, вроде{"."*10}")
print("Тест соединения прошёл:", res)

# m.main_cycle()
    
