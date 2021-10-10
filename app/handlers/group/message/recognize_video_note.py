import os

import speech_recognition as speech_recog
from aiogram import Dispatcher, F

__all__ = ['setup']

from aiogram.types import Message
from moviepy.video.io.VideoFileClip import VideoFileClip

from speech_recognition import Recognizer

from settings import TMP_DIR, DEFAULT_LOCALE


async def recognize_video_note(msg: Message, _, bot):
    msg_recognize_voice = await msg.reply(
        _('Секунду, сейчас переведу в текст...')
    )

    path_to_video_note_mp4 = f'{TMP_DIR}/{msg.video_note.file_id}.mp4'

    await bot.download(msg.video_note.file_id, path_to_video_note_mp4)
    video = VideoFileClip(path_to_video_note_mp4)
    voice = video.audio

    path_to_voice_wav = f'{TMP_DIR}/{msg.video_note.file_id}.wav'
    voice.write_audiofile(path_to_voice_wav)

    sample_audio = speech_recog.AudioFile(path_to_voice_wav)

    with sample_audio as audio_file:
        recog = Recognizer()
        audio_content = recog.record(audio_file)
        try:
            voice_text = recog.recognize_google(audio_content, language=DEFAULT_LOCALE)
        except:
            voice_text = _('Мне не удалось распознать, говорите внятней!')
    await msg_recognize_voice.edit_text(voice_text)
    os.remove(path_to_video_note_mp4)
    os.remove(path_to_voice_wav)


def setup(dp: Dispatcher, *args, **kwargs):
    dp.message.register(
        recognize_video_note, F.chat.type.in_(('supergroup', 'group')), content_types=['video_note']
    )
