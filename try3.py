import threading, time
from datetime import datetime

count = 2


def delayed():
    global count
    th_name = threading.current_thread().name
    print('*' * 40)
    print(f'Th: {th_name} Worker запущен')
    print('active thread:', threading.active_count())
    print('currentThread():', threading.currentThread(), 'enumerate:', threading.enumerate())
    print('Now time:', datetime.now())
    print('*' * 40)
    count += 1
    t = threading.Timer(2, delayed)
    t.name = f'Timer-{count}'
    t.start()


# Создание и запуск потоков таймеров
t1 = threading.Timer(3, delayed)
t1.name = 'Timer-1'
t2 = threading.Timer(6, delayed)
t2.name = 'Timer-2'

print('\tЗапуск таймеров')

print(f'Main thread: {threading.main_thread()}; Name: {threading.main_thread().name}')
print('active thread:', threading.active_count())
print('enumerate:', threading.enumerate())
print('currentThread():', threading.currentThread())

t1.start()
t2.start()
print('enumerate after start:', threading.enumerate())

print(f'Ожидание перед завершением {t2.name}')
time.sleep(1)
print(f'Завершение {t2.name}')
# t2.cancel()
print('Выполнено')
