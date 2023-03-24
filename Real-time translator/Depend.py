from googletrans import Translator
from pynput import keyboard
from pynput.keyboard import Key, KeyCode, Listener, Controller
import ctypes
import pyperclip
import keyboard as kb
import time
from key_lay_dict import KEY_LAY_DICT

user32 = ctypes.WinDLL('user32', use_last_error=True)


words = ''
past_key = ''


def get_keyboard_language() -> str:
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


def is_rus() -> bool:
    lang_id = get_keyboard_language()  # 0x409 -> en; 0x419 -> ru
    if lang_id == '0x419':
        return True
    else:
        return False


def display_info(key) -> None:
    try:
        print(f'{key}:{key.char} pressed; {type(key)}:{type(key.char)}')
    except AttributeError:
        print(f'special key {key} pressed; {type(key)}')

    print(f"\n\tKey: {key}"
          f"\n\tType: {type(key)}: {type(type(key))}"
          f"\n\tName: {type(key).__name__}: {type(type(key).__name__)}"
          f"\n\twas raised: {key}\n")


def text_translator(text='Hello friend', src='en', dest='ru') -> str:
    try:
        translator = Translator()
        translation = translator.translate(text=text, src=src, dest=dest)
        return translation.text
    except Exception as ex:
        print(f'\tError:\tName: {type(ex).__name__}\tType: {type(ex)} was raised: {ex}')
        return 'ERROR!'


def on_press(key):
    global words, past_key

    if type(key).__name__ == 'KeyCode' and past_key != Key.ctrl_l:
        try:
            if is_rus():
                words += KEY_LAY_DICT[key.char]
            else:
                words += key.char
        except Exception as ex:
            print('\tError on_press:', type(ex).__name__, type(ex), ex)

    if key == Key.backspace:  # and type(key).__name__ == 'Key'
        words = words[:-1]
    if key == Key.space:
        words += ' '
    if key == Key.enter:
        words += '\n'
        ctypes.windll.user32.BlockInput(True)
        time.sleep(3)
        ctypes.windll.user32.BlockInput(False)
    past_key = key

    # display_info(key)


def on_release(key):
    global words
    print(f'{words=}')
    # print(f'{key} release; {type(key)}')
    if key == Key.esc:
        print(f'\tWords: \n{words};')
        # Stop listener
        # return False
        exit()
    if key == Key.space:
        ans = text_translator(text=words, src='ru', dest='en') + ' '
        print(f'\tWords: {words}\n\tAnswer: {ans}')
        pyperclip.copy(ans)
        kb.press_and_release('ctrl+a, ctrl+v')

        # key_controller = Controller()
        # key_controller.press('A')
        # key_controller.release('A')
        # with key_controller.pressed(Key.shift):
        #     key_controller.press('a')
        #     key_controller.release('a')

    if key == Key.enter:
        words = ''


# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# Смотреть видео ошибки, проверить пробел после вставки слова, история запуск почему, добавить перевод по копи паст
