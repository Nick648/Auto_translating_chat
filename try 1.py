from googletrans import Translator
from pynput import keyboard
from pynput.keyboard import Key, Listener, Controller
import ctypes
import pyperclip
import keyboard as kb

user32 = ctypes.WinDLL('user32', use_last_error=True)

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

'''
KEY_LAY_DICT = {
    'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ',
    'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж', "'": 'э', 
    'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю', '/': '.', 
    '`': 'ё', 
    '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '0': '0', '-': '-', '=': '=', 
    
    'Q': 'Й', 'W': 'Ц', 'E': 'У', 'R': 'К', 'T': 'Е', 'Y': 'Н', 'U': 'Г', 'I': 'Ш', 'O': 'Щ', 'P': 'З', '{': 'Х', '}': 'Ъ', 
    'A': 'Ф', 'S': 'Ы', 'D': 'В', 'F': 'А', 'G': 'П', 'H': 'Р', 'J': 'О', 'K': 'Л', 'L': 'Д', ':': 'Ж', '"': 'Э', 
    'Z': 'Я', 'X': 'Ч', 'C': 'С', 'V': 'М', 'B': 'И', 'N': 'Т', 'M': 'Ь', '<': 'Б', '>': 'Ю', '?': ',', 
    '~': 'Ё', 
    '!': '!', '@': '"', '#': '№', '$': ';', '%': '%', '^': ':', '&': '?', '*': '*', '(': '(', ')': ')', '_': '_', '+': '+'
}
'''

words = ''


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


def display_info(key):
    print(f"\n\tKey: {key}"
          f"\n\tType: {type(key)}: {type(type(key))}"
          f"\n\tName: {type(key).__name__}: {type(type(key).__name__)}"
          f"\n\twas raised: {key}\n")


def text_translator(text='Hello friend', src='en', dest='ru'):
    try:
        translator = Translator()
        translation = translator.translate(text=text, src=src, dest=dest)
        return translation.text
    except Exception as ex:
        print(f'\tError:\tName: {type(ex).__name__}\tType: {type(ex)} was raised: {ex}')
        return 'ERROR!'


past_key = ''


def on_press(key):
    global words, past_key

    if type(key).__name__ == 'KeyCode' and past_key != Key.ctrl_l:
        try:
            if is_rus():
                words += KEY_LAY_DICT[key.char]
            else:
                words += key.char
        except Exception as ex:
            print('\t', type(ex).__name__, type(ex), ex)

    if key == Key.backspace:  # and type(key).__name__ == 'Key'
        words = words[:-1]
    if key == Key.space:
        words += ' '
    if key == Key.enter:
        words += '\n'
    past_key = key

    # display_info(key)

    # try:
    #     print(f'{key}:{key.char} pressed; {type(key)}:{type(key.char)}')
    # except AttributeError:
    #     print(f'special key {key} pressed')


def on_release(key):
    global words
    # print(f'{key} release; {type(key)}')
    if key == Key.esc:
        print(f'\tWords: \n{words};')
        # Stop listener
        return False
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
