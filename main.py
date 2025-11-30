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

    def __init__(self): # X
        DbTable.dbconn = self.connection
        return

    def db_init(self): # X
        colt = CollectionsTable()
        ext = ExhibitsTable()
        colt.create()
        ext.create()
        return

    def db_insert_somethings(self): # X
        colt = CollectionsTable()
        ext = ExhibitsTable()

        #  Не забыть, что надо также проверять валидность данных
        colt.insert_one({
            "name": "Челябинский метеорит и космо-наследие",
            "description": "Коллекция, посвящённая знаменитому челябинскому метеориту — его фрагменты, история падения и исследования."
        })

        colt.insert_one({
            "name": "История быта и культуры Южного Урала",
            "description": "Экспозиция, отражающая народный быт, этнографию и культуру населения края."
        })

        colt.insert_one({
            "name": "XX век: индустриализация и война",
            "description": "Коллекция, посвящённая истории Урала в XX веке: промышленность, война, советский период."
        })
        ext.insert_one({
            "name": "Фрагмент метеорита Чебаркуль",
            "description": "Кусок метеорита, найденного в Челябинской области после падения в озеро Чебаркуль.",
            "insurance_value": 1000000.00,
            "century": 21,
            "collection_id": 1,
            "hall_id": 5,
            "height": 50.00,
            "width": 40.00,
            "length": 25.00,
            "need_temp_control": "n",
            "need_humidity_control": "n",
            "protected_from_people": "y"
        })
        ext.insert_one({
            "name": "Керамический горшок XIX века",
            "description": "Глиняный горшок из крестьянского быта Южного Урала.",
            "insurance_value": 5000.00,
            "century": 19,
            "collection_id": 2,
            "hall_id": 2,
            "height": 30.00,
            "width": 30.00,
            "length": 30.00,
            "need_temp_control": "n",
            "need_humidity_control": "n",
            "protected_from_people": "y"
        })
        ext.insert_one({
            "name": "Плакат индустриализации Урала",
            "description": "Плакат советского периода, демонстрирующий развитие промышленности.",
            "insurance_value": 12000.00,
            "century": 20,
            "collection_id": 3,
            "hall_id": 3,
            "height": 80.00,
            "width": 60.00,
            "length": 1.00,
            "need_temp_control": "n",
            "need_humidity_control": "n",
            "protected_from_people": "y"
        })

    def db_drop(self): # X
        colt = CollectionsTable()
        ext = ExhibitsTable()
        ext.drop()
        colt.drop()
        return

    def show_main_menu(self): # X
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр коллекций;
    2 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
        return

    def read_next_step(self): # X
        return input("=> ").strip()

    def after_main_menu(self, next_step): # X
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

    def print_menu(self, menu): # X
        for k, v in menu.items():
            print(k, v)

    # Collections UI ===================
    @table_paginator(page_size=3)
    def show_collections(self): # X
        table = CollectionsTable()
        return table, table.columns(), table.all()

    def after_show_collections_menu(self): # X
        menu = {
            "3": "Добавить коллекцию",
            "4": "Удалить коллекцию",
            "5": "Просмотр экспонатов коллекции",
            "6": "Редактировать коллекцию",
            "0": "Возврат в главное меню",
            "9": "Выход"
        }
        self.print_menu(menu)

    def after_show_collections(self, cmd):
        menu = {
            "3": "Добавить коллекцию",
            "4": "Удалить коллекцию",
            "5": "Просмотр экспонатов коллекции",
            "6": "Редактировать коллекцию",
            "0": "Возврат в главное меню",
            "9": "Выход"
        }

        self.print_menu(menu)

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
        print("Добавление коллекции (q — отмена, Null = NULL)")

        name = input_text("Название: ")
        if name == "quit":
            return

        description = input_text("Описание: ")
        if description == "quit":
            return

        data = {
            "name": name,
            "description": description,
        }

        CollectionsTable().insert_one(data)
        # print("Коллекция добавлена.")

    def choose_collection_by_row(self):
        lst = CollectionsTable().all()
        if not lst:
            print("Список коллекций пуст.")
            return None
        while True:
            num = input_num("Укажите номер строки коллекции (0 - отмена): ", onlyint=True)
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
        row = self.choose_collection_by_row()
        print(row)
        if not row:
            print("Не найдено.")
            return

        data = {}
        colmap = {"name": row[1], "description": row[2]}

        for col, old in colmap.items():
            raw = input_text(f"{col} [{old}] (ENTER = NULL): ")
            if raw == "quit":
                return
            data[col] = raw  # None = NULL, строка = новое

        CollectionsTable().update_ents(("id", row[0]), data)
        print("Запись обновлена.")

    def show_add_collection(self):
        # Не реализована проверка на максимальную длину строк. Нужно доделать самостоятельно!
        name = input_text("Введите название коллекции (1 - отмена): ")
        if name is None:
            return

        desc = input_text("Введите описание (ENTER для пустого, 1 - отмена): ")
        if desc is None:
            return
        CollectionsTable().insert_one({"name":name, "description":desc})
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
        print("Добавление экспоната (q — отмена, ENTER = default)")

        name = input_text("Название: ")
        if name == "quit": return

        description = input_text("Описание (enter = 0): ")
        if description == "quit": return

        insurance_value = input_num("Страховая стоимость (enter = 0): ")
        if insurance_value == "quit": return

        century = input_num("Век (<21): ", onlyint=True)
        if century == "quit": return

        hall_id = input_num("Номер зала: ", onlyint=True)
        if hall_id == "quit": return

        height = input_num("Высота (>0): ")
        if height == "quit": return

        width = input_num("Ширина (>0): ")
        if width == "quit": return

        length = input_num("Длина (>0): ")
        if length == "quit": return

        need_temp = input_yn("Требуется контроль температуры (enter = y) y/N?")
        if need_temp == "quit": return

        need_hum = input_yn("Требуется контроль влажности (enter = y) y/N?")
        if need_hum == "quit": return

        protected = input_yn("Защита от людей (enter = y) y/N?")
        if protected == "quit": return

        data = {
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
            "protected_from_people": protected
        }

        ExhibitsTable().insert_one(data)
        print("Экспонат добавлен.")

    def delete_exhibit_from_list(self, lst):
        if not lst:
            print("Нет экспонатов для удаления.")
            return
        while True:
            num = input_num("Номер строки экспоната для удаления (0 - отмена): ", onlyint=True )
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
            print("Нет экспонатов.")
            return

        pos = input_num("Номер строки (q — отмена): ", onlyint=True)
        if pos == "quit": return

        rec = ExhibitsTable().find_by_position(int(pos))
        if rec is None:
            print("Неверный номер.")
            return

        ex_id = rec[0]
        print(f"Редактирование экспоната: {rec[1]}")

        old = {
            "name": rec[1],
            "description": rec[2],
        }

        data = {}
        for col, oldv in old.items():
            raw = input_text(f"{col} [{oldv}] (ENTER = NULL): ")
            if raw == "quit": return
            data[col] = raw

        ExhibitsTable().update_ents(ex_id, data)
        print("Экспонат обновлён.")

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
                self.after_show_collections_menu()
                next_step = self.read_next_step()
                current_menu = self.after_show_collections(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.show_add_collection()
                current_menu = "1"
            elif current_menu == "5":  # <<< ЭТО ДОБАВИТЬ
                coll_ctx, rows = self.show_exhibits_by_collection()
                current_menu = self.after_show_exhibits(coll_ctx, rows)

        print("До свидания!")
        return

    def test(self):
        DbTable.dbconn.test()

m = Main()
# Откоментируйте эту строку и закоментируйте следующую для теста
# соединения с БД
# res = m.connection.test()
# print("Тест соединения прошёл:", res)
print(f"Подключилось, вроде{"."*10}")

m.main_cycle()
    
