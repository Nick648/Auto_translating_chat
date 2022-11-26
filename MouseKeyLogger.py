import threading
import time
from datetime import datetime
from pynput import mouse, keyboard
from pynput.keyboard import Key, Controller

# time.sleep(2)
# key_controller = Controller()
# key_controller.press('A')
# key_controller.release('A')
# with key_controller.pressed(Key.shift):
#     key_controller.press('a')
#     key_controller.release('a')

today = datetime.today()
date_y, date_m, date_d = today.year, today.month, today.day
MOUSE_REPORT_FILE = f'MouseLogger {date_d}_{date_m}_{str(date_y)[-2:]}.txt'
KEYBOARD_REPORT_FILE = f'KeyLogger {date_d}_{date_m}_{str(date_y)[-2:]}.txt'
ENCODE = 'utf-8'


def create_report_files():
    with open(file=MOUSE_REPORT_FILE, mode='w', encoding=ENCODE) as _:
        pass
    with open(file=KEYBOARD_REPORT_FILE, mode='w', encoding=ENCODE) as _:
        pass


def report_to_file(name_file, report):
    today = datetime.today()
    date_y, date_m, date_d = today.year, today.month, today.day
    time_h, time_m, time_s = today.hour, today.minute, today.second
    report += '\n'
    with open(file=name_file, mode='a', encoding=ENCODE) as file:
        file.write(f'{date_d:2}.{date_m:2}.{date_y:4} {time_h:2}:{time_m:2}:{time_s:2} >>> {report}')


def on_move(x, y):
    report = 'Pointer moved to {0}'.format((x, y))
    report_to_file(MOUSE_REPORT_FILE, report)


def on_click(x, y, button, pressed):
    if pressed:
        func = 'Pressed'
    else:
        func = 'Released'
    report = f'{func} at {(x, y)}, Button: {button} -> {type(button)}'
    report_to_file(MOUSE_REPORT_FILE, report)
    if not pressed:
        report_to_file(MOUSE_REPORT_FILE, 'Stop Mouse Listener')
        # Stop Mouse Listener
        return False


def on_scroll(x, y, dx, dy):
    if dy < 0:
        place = 'down'
    else:
        place = 'up'
    report = f'Scrolled {place} at {(x, y)}; {dx=}, {dy=}'
    report_to_file(MOUSE_REPORT_FILE, report)


def on_press(key):
    report = 'on_press'
    try:
        report = f'{key}:{key.char} pressed; {type(key)}:{type(key.char)}'
    except AttributeError:
        report = f'special key {key} pressed; {type(key)}'
    finally:
        report_to_file(KEYBOARD_REPORT_FILE, report)


def on_release(key):
    report = f'{key} release; {type(key)}'
    report_to_file(KEYBOARD_REPORT_FILE, report)
    if key == Key.esc:
        report_to_file(KEYBOARD_REPORT_FILE, 'Stop Keyboard Listener')
        # Stop Keyboard Listener
        return False


def listen_mouse():
    # Collect events until released
    with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        listener.join()


def listen_keyboard():
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


def main():
    create_report_files()
    thr_mouse = threading.Thread(target=listen_mouse, name=f'thr-mouse')  # , args=(str(time.time()), i,)
    thr_keyboard = threading.Thread(target=listen_keyboard, name=f'thr-keyboard')  # , args=(str(time.time()), i,)
    thr_mouse.start()
    thr_keyboard.start()

    for i in range(15):
        print(f'{i}) {"*" * 30}')
        print('Active thread:', threading.active_count())
        print('Enumerate:', threading.enumerate())
        time.sleep(3)

    # print(thr_mouse.is_alive())
    # print(thr_mouse.isDaemon())


if __name__ == '__main__':
    main()
