import pyttsx3
from pydub import AudioSegment


def engine_settings(engine, article_language):
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 185)  # Выставляем скорость чтения голоса
    for voice in voices:
        if voice.languages == article_language and \
                voice.gender == 'VoiceGenderMale':
            return engine.setProperty('voice', voice.id)  # Выбираем подходящий голос


def get_mp3_file(file_name, article_text, article_language):
    engine = pyttsx3.init()
    engine_settings(engine, article_language)  # Применение настроек голоса
    engine.save_to_file(article_text, file_name)  # Сохранение текста статьи в аудиофайл
    engine.runAndWait()
    convert_file_to_mp3(file_name)  # Конвертация в mp3 формат


def convert_file_to_mp3(file_name):
    converter = AudioSegment
    converter_file = converter.from_file(file_name)
    converter_file.export(file_name, format="mp3")

