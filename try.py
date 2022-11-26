import keyboard

import time


keyboard.press_and_release('ctrl+a, ctrl+v')


translate = {
    'down': ' нажал на клавишу ',
    'up': ' отпустил клавишу '
}


def print_pressed_keys(e):
    print(
        'Пользователь {}{} -> {}'.format(translate[e.event_type], e.name, e)
    )


# keyboard.hook(print_pressed_keys)
# keyboard.wait()

from pynput import keyboard


def on_activate_sa():
    print('Нажато сочетание клавиш: <shift>+<alt>')


def on_activate_i():
    print('Нажато сочетание клавиш: <ctrl>+<alt>+i')


with keyboard.GlobalHotKeys({
    '<shift>+<alt>': on_activate_sa,
    '<ctrl>+<alt>+i': on_activate_i}) as h:
    h.join()
