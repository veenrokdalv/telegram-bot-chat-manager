import speech_recognition as speech_recog
from aiogram.utils.i18n import I18n

from settings import DEFAULT_LOCALE


def get_text_from_audio_file(_: I18n.gettext, path_to_audio_wav, default: str = None) -> str:
    sample_audio = speech_recog.AudioFile(path_to_audio_wav)
    with sample_audio as audio_file:
        recog = speech_recog.Recognizer()
        audio_content = recog.record(audio_file)
        try:
            _text = recog.recognize_google(audio_content, language=DEFAULT_LOCALE)
        except:
            if not default:
                _text = _('Мне не удалось распознать, говорите внятней!')
            else:
                _text = _(default)
    return _text
