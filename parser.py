from langdetect import detect

def get_article_language(article_text):
    # return detect(article_text)
    try:
        language = detect(article_text)  # Определяем язык статьи
    except TypeError:
        return False
    else:
        if language == 'bg':
            return ['Русский', ['ru_RU']]
        elif language == 'ru':
            return ['Русский', ['ru_RU']]
        else:
            return ['Английский', ['en_GB']]

# article_text = 'hello world'
# article_language = get_article_language(article_text)
#
# print(article_language)