import threading
import time

class Printer:
    def __init__(self):
        self.printer_locks = [threading.Semaphore(1) for _ in range(2)]
    
    def request(self):
        printer_id = -1
        # Чекаємо, поки один з двох принтерів звільниться
        for i, lock in enumerate(self.printer_locks):
            if lock.acquire(blocking=False):
                printer_id = i
                break
        # Повертаємо ідентифікатор вільного принтера
        return printer_id
    
    def release(self, printer_id):
        # Звільняємо принтер, щоб його міг використати інший користувач
        self.printer_locks[printer_id].release()

def print_job(printer_id, user_id):
    print(f"\nКористувач {user_id} друкує на принтері. ")
    # Моделюємо роботу принтера
    time.sleep(0)
    print(f"\nКористувач {user_id} закінчив друк на принтері. ")
    printers.release(printer_id)

def user_job(user_id):
    # Запитуємо доступ до принтера
    printer_id = printers.request()
    print(f"\nКористувач {user_id} отримав принтер. ")
    # Моделюємо друк на принтері
    print_job(printer_id, user_id)

# Створюємо об'єкт Printer
printers = Printer()

# Створюємо список користувачів
users = [1, 2, 3, 4, 5]

# Створюємо потоки для кожного користувача
threads = []
for user in users:
    thread = threading.Thread(target=user_job, args=(user,))
    threads.append(thread)

# Запускаємо потоки
for thread in threads:
    thread.start()

# Очікуємо завершення всіх потоків
for thread in threads:
    thread.join()

print("Усі користувачі завершили друк.")