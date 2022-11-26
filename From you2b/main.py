from googletrans import Translator, LANGCODES, LANGUAGES

# print(help(Translator))
print(f'LANGUAGES: {type(LANGUAGES)}, {len(LANGUAGES)}, {LANGUAGES}'
      f'\nLANGCODES: {type(LANGCODES)}, {len(LANGCODES)}, {LANGCODES}')


def output_dict(dic, name):
    print(f'\n{name}:')
    for key, value in dic.items():
        print(f'\t{key}: {value}')


def text_translator(text='Hello friend', src='en', dest='ru'):
    try:
        translator = Translator()
        translation = translator.translate(text=text, src=src, dest=dest)
        return translation.text
    except Exception as ex:
        return f'\tError:\tType: {type(ex)}\tName: {type(ex).__name__} was raised: \n{ex}'


def main():
    print(f'\n>>> ', end='')
    print(text_translator(text='Hello', src='en', dest='fr'))


if __name__ == '__main__':
    # output_dict(LANGUAGES, 'LANGUAGES')
    # output_dict(LANGCODES, 'LANGCODES')
    main()
