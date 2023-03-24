import keyboard
from googletrans import Translator
from pynput import keyboard
import time


def check_translator(text='Hello friend', src='en', dest='ru') -> str:
    # translator = Translator(service_urls=['translate.googleapis.com'])
    translator = Translator()
    translation = translator.translate(text=text, src=src, dest=dest)
    # translation = translator.translate(text=text)
    dec_lan = translator.detect('привет')
    print(f'{dec_lan=}')
    print(f'{translation=}\n'
          f'{translation.src=}; {translation.dest=}; {translation.origin=}\n'
          f'{translation.text=}; {translation.pronunciation=};')


def check_keyboard():
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


def check_pynput():
    def on_activate_sa():
        print('Нажато сочетание клавиш: <shift>+<alt>')

    def on_activate_i():
        print('Нажато сочетание клавиш: <ctrl>+<alt>+i')

    with keyboard.GlobalHotKeys({
        '<shift>+<alt>': on_activate_sa,
        '<ctrl>+<alt>+i': on_activate_i}) as h:
        h.join()


if __name__ == '__main__':
    # check_keyboard()
    # check_pynput()
    check_translator('привет', 'ru', 'en')
