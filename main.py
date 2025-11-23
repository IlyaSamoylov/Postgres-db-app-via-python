import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *
from tables.collections_table import *
from tables.exhibits_table import *
from utils import *

#  TODO: Пересмотреть и исправить методы с people/phone на collections/exhibits
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
    #  TODO: сравнить потом с пробой. Проверить реализацию перелистывания
    def show_collections(self, page=1, page_size=5):
        # self.collection_id = -1

        lst = CollectionsTable().all()

        print("""Просмотр списка коллекций!\n№\tНазвание\tОписание""")

        menu = {"": "Дальнейшие операции -",
                "<": "- пролистнуть влево;",
                ">": "- пролистнуть вправо;",
                "0": "- возврат в главное меню;",
                "3": "- добавление новой коллекции;",
                "4": "- удаление коллекции;",
                "5": " - просмотр экспонатов коллекции;",
                "9": "- выход."
                }

        start = (page - 1) * page_size
        end = (page * page_size) - 1

        for idx, row in enumerate(lst[start:end+1], 1) :
            name = row[1]
            desc = row[2] if row[2] is not None else ""
            print(f"{idx}\t{name}\t{desc}")
        print(f"Показана {page} страница")

        # TODO: Проверить перелистывание страниц
        self.print_menu(menu)

        inp = input("Что дальше?").strip()
        # я сдался, не смог здесь написать match-case
        if inp == ">" and page < len(lst):
            self.show_collections(page + 1)
        elif inp == "<" and page > 1:
            self.show_collections(page-1)
        elif inp in menu.keys():
            return
        else:
            print("Неизвестная команда")

        # menu = """Дальнейшие операции:
        #     < - пролистнуть влево;
        #     > - пролистнуть вправо;
        #     0 - возврат в главное меню;
        #     3 - добавление новой коллекции;
        #     4 - удаление коллекции;
        #     5 - просмотр экспонатов коллекции;
        #     9 - выход."""
        # print(menu)
        return
    # TODO: Добавить всякие там удаления, добавления, выводы и прочий доп, который в классе таблиц писал
    def after_show_collections(self, next_step):
        while True:
            if next_step == "4":
                print("Пока не реализовано!")
                return "1"
            elif next_step == "6" or next_step == "7":
                print("Пока не реализовано!")
                next_step = "5"
            elif next_step == "5":
                next_step = self.show_exhibits_by_collection()
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    # TODO: Перепроверить. Статичные?
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

        # data = []
        # data.append(input("Введите имя (1 - отмена): ").strip())
        # if data[0] == "1":
        #     return
        # while len(data[0].strip()) == 0:
        #     data[0] = input("Имя не может быть пустым! Введите имя заново (1 - отмена):").strip()
        #     if data[0] == "1":
        #         return
        # data.append(input("Введите фамилию (1 - отмена): ").strip())
        # if data[1] == "1":
        #     return
        # while len(data[1].strip()) == 0:
        #     data[1] = input("Фамилия не может быть пустой! Введите фамилию заново (1 - отмена):").strip()
        #     if data[1] == "1":
        #         return
        # data.append(input("Введите отчество (1 - отмена):").strip())
        # if data[2] == "1":
        #     return
        # CollectionsTable().insert_one(data)
        return

    #  Exhibits UI ===================
    def show_exhibits_by_collection(self):
        # if self.person_id == -1:    # TODO: Разобраться, зачем все таки был нужен person_id
        #     while True:
        #         num = input("Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
        #         while len(num.strip()) == 0:
        #             num = input("Пустая строка. Повторите ввод! Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
        #         if num == "0":
        #             return "1"
        #         person = CollectionsTable().find_by_position(int(num))
        #         if not person:
        #             print("Введено число, неудовлетворяющее количеству людей!")
        #         else:
        #             self.person_id = int(person[1])
        #             self.person_obj = person
        #             break
        # print("Выбран человек: " + self.person_obj[2] + " " + self.person_obj[0] + " " + self.person_obj[3])
        # print("Телефоны:")
        # lst = ExhibitsTable().all_by_person_id(self.person_id)
        # for i in lst:
        #     print(i[1])
        #     menu = """Дальнейшие операции:
        # 0 - возврат в главное меню;
        # 1 - возврат в просмотр людей;
        # 6 - добавление нового телефона;
        # 7 - удаление телефона;
        # 9 - выход."""
        #     print(menu)
        #     return self.read_next_step()
        #
        # return self.read_next_step()
        # TODO: Пролистывание страниц. Может, написать через декоратор?
        coll = self.choose_collection_by_row()
        if coll is None:
            return
        coll_id = coll[0]
        print(f"Экспонаты коллекции: {coll[1]}")
        lst = ExhibitsTable().select_by_col_id(coll_id)
        if not lst:
            print("Экспонатов нет.")
            return
        for idx, row in enumerate(lst, start=1):
            # assume row structure: (id, name, description, ...)
            name = row[1] if len(row) > 1 else ""
            desc = row[2] if len(row) > 2 else ""
            print(f"{idx}\t{name}\t{desc}")

        menu = """Дальнейшие операции:
            0 - возврат в главное меню;
            1 - возврат в просмотр коллекций;
            6 - добавление нового экспоната;
            7 - удаление экспоната;
            8 - редактирование экспоната;
            9 - выход."""
        print(menu)
        cmd = self.read_next_step()
        if cmd == "6":
            self.add_exhibit_to_collection(coll_id)
        elif cmd == "7":
            self.delete_exhibit_from_list(lst)
        elif cmd == "8":
            self.edit_exhibit_in_list(lst)

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
        while(current_menu != "9"):
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
                self.show_add_person()
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
    
