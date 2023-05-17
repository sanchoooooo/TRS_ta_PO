import threading

class Printers:
    def __init__(self):
        self.printer_available = [1, 2]  # Список доступних принтерів
        self.lock = threading.Lock()  # Створюємо блокування

        # Створюємо умову (Condition), яку будемо використовувати для синхронізації
        self.printer_condition = threading.Condition(self.lock)

    def request(self):
        with self.printer_condition:
            while not self.printer_available:  # Поки не буде вільного принтера, чекаємо
                self.printer_condition.wait()
            printer_id = self.printer_available.pop()  # Беремо доступний принтер
            print(f"\nПринтер {printer_id} зараз використовується.")
            return printer_id

    def release(self, printer_id):
        with self.printer_condition:
            self.printer_available.append(printer_id)  # Повертаємо принтер
            print(f"\nПринтер {printer_id} тепер доступний.")
            self.printer_condition.notify()  # Сповіщаємо інші потоки, що принтер знову доступний


def user_job(printers, user_id):
    printer_id = printers.request()
    # Виконуємо друковану роботу
    print(f"\nКористувач {user_id} друкує за допомогою принтера {printer_id}")
    # time.sleep(1)  # Затримка для симуляції друкованої роботи
    printers.release(printer_id)

if __name__ == '__main__':
    printers = Printers()  # Створюємо екземпляр класу Printers
    users = []  # Створюємо список користувачів
    for i in range(5):
        users.append(threading.Thread(target=user_job, args=(printers, i+1)))
        users[-1].start()  # Запускаємо потік
    for user in users:
        user.join()  # Завершуємо потік