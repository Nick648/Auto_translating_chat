from googletrans import Translator, LANGCODES, LANGUAGES
from pynput.keyboard import Key, KeyCode, Listener


def display_info_module(module) -> None:
    print(help(module))
    output_dict(LANGUAGES, 'LANGUAGES')
    output_dict(LANGCODES, 'LANGCODES')


def output_dict(dic: dict, name: str) -> None:
    print(f'\n{name}:')
    print(f'{name}: {type(dic)}, {len(dic)}, dict = {dic}')
    for key, value in dic.items():
        print(f'\t{key}: {value}')


def display_all_lang_translate() -> None:
    count_lang = 1
    print(f'\n\tПеревод фразы: "Привет! Как дела?" на все доступные языки.')
    print(f'\nЯзыки: \n\tКоличество языков = {len(LANGUAGES)}\n')
    for key, value in LANGUAGES.items():
        ans = text_translator(text='Привет! Как дела?', src='ru', dest=key)
        print(f'{count_lang:4}\t{key:5}: {value:21}  ->  {ans}')
        count_lang += 1


def lang_detect() -> None:
    from langdetect import detect, detect_langs
    lang = detect("привет")
    print(lang)


def text_translator(text: str = 'Hello friend', src: str = 'en', dest: str = 'ru') -> str:
    try:
        translator = Translator()
        translation = translator.translate(text=text, src=src, dest=dest)
        return translation.text
    except Exception as ex:
        print(f'\tError:\tType: {type(ex)}\tName: {type(ex).__name__} was raised: \n{ex}')
        return 'ERROR!'


def test_translator() -> None:
    print('\n>>>', text_translator())
    print('\n>>>', text_translator(text='Hello', src='en', dest='fr'))


def listen_keyboard():  # В этом блоке будет работать слушатель событий.
    global words

    def display_info(key) -> None:
        print(f"\n\tKey: {key}"
              f"\n\tType: {type(key)}"
              f"\n\tName: {type(key).__name__}: {type(type(key).__name__)}"
              f"\n\twas raised: {key}\n")

    def on_press(key):
        global words

        if type(key).__name__ == 'KeyCode':
            words += key.char
        if type(key).__name__ == 'Key' and key == Key.space:
            words += ' '
        if type(key).__name__ == 'Key' and key == Key.backspace:
            words = words[:-1]
            print(words)

        display_info(key)

        try:
            print(f'{key}:{key.char} pressed; {type(key)}:{type(key.char)}')
        except AttributeError:
            print(f'special key {key} pressed')

    def on_release(key):
        # print(f'{key} release; {type(key)}')
        if key == Key.esc:
            # Stop listener
            # return False
            exit()

        if key == Key.space:
            ans = text_translator(text=words, src='ru', dest='en')
            if ans == 'ERROR!':
                print(f'Word: {words}\tAnswer: {words}')
            else:
                print(f'Word: {words}\tAnswer: {ans}')

    # Collect events until released
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


if __name__ == '__main__':
    words = ''
    listen_keyboard()
    # display_info_module(googletrans)
    # display_all_lang_translate()
    # test_translator()
