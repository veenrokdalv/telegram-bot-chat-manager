import asyncio
import concurrent.futures
import os

from aiogram import Dispatcher, Bot, F

__all__ = ['setup']

from aiogram.types import Message
from moviepy.editor import AudioFileClip

from app.utils.misc.recognize_audio import get_text_from_audio_file
from settings import TMP_DIR


async def recognize_voice(msg: Message, _, bot: Bot):
    msg_recognize_voice = await msg.reply(
        _('Секунду, сейчас переведу в текст...')
    )

    path_to_voice_ogg = f'{TMP_DIR}/{msg.voice.file_id}.ogg'

    await bot.download(msg.voice.file_id, path_to_voice_ogg)
    voice = AudioFileClip(path_to_voice_ogg)

    path_to_voice_wav = f'{TMP_DIR}/{msg.voice.file_id}.wav'
    voice.write_audiofile(path_to_voice_wav)

    with concurrent.futures.ThreadPoolExecutor() as pool:
        loop = asyncio.get_running_loop()
        voice_text = await loop.run_in_executor(pool, get_text_from_audio_file, _, path_to_voice_wav)

    await msg_recognize_voice.edit_text(voice_text)
    os.remove(path_to_voice_ogg)
    os.remove(path_to_voice_wav)


def setup(dp: Dispatcher, *args, **kwargs):
    dp.message.register(recognize_voice, F.chat.type.in_(('supergroup', 'group')), content_types=['voice'])
