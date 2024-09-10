import time
from threading import Thread
from random import randint
import queue

print('\033[30m\033[47mДомашнее задание по теме "Очереди для обмена данными между потоками."\033[0m')
print('\033[30m\033[47mЗадача "Потоки гостей в кафе":\033[0m')
print('Студент: \033[30m\033[47mКрылов Эдуард Васильевич\033[0m')
print('Дата: \033[30m\033[47m10.09.2024 года.\033[0m')
thanks = '\033[30m\033[47mБлагодарю за внимание :-)\033[0m'
print()

# Пример результата выполнения программы:
# Выполняемый код:


class Table:
    def __init__(self, number):
        self.number = number
        self.quest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time.sleep(randint(3, 10))


class Cafe:
    list_quest = []

    def __init__(self, *table):
        self.queue = queue.Queue()
        self.tables = list(table)

    def guest_arrival(self, *guest):
        len_guests = len(list(guest))
        guests_tables = min(len_guests, len(self.tables))
        for i in range(guests_tables):
            self.tables[i].guest = guest[i]
            set_thr = guest[i]
            set_thr.start()
            Cafe.list_quest.append(set_thr)
            print(f'\033[32m{list(guest)[i].name} сел(-а) за стол номер {self.tables[i].number}\033[0m')
        if len_guests > guests_tables:
            for q in range(guests_tables, len_guests):
                self.queue.put(guest[q])
                print(f'\033[34m{list(guest)[q].name} в очереди\033[0m')

    def discuss_guests(self):
        while not (self.queue.empty()) or Cafe.check_table(self):
            for table in self.tables:
                if not (table.guest is None) and not (table.guest.is_alive()):
                    print(f'\033[32m{table.guest.name} покушал(-а) и ушёл(ушла)\033[0m')
                    print(f'\033[31mСтол номер {table.number} свободен\033[0m')
                    table.guest = None
                if not (self.queue.empty()) and table.guest is None:
                    table.guest = self.queue.get()
                    print(f'\033[33m{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер '
                          f'{table.number}\033[0m')
                    set_thr = table.guest
                    set_thr.start()
                    Cafe.list_quest.append(set_thr)

    def check_table(self):
        for table in self.tables:
            if table.guest is not None:
                return True
        return False


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman', 'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya',
                'Alexandra', 'Эдуард']
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
# Благодарность

print()
print(thanks)
