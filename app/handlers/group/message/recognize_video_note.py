import os

from aiogram import Dispatcher, F

__all__ = ['setup']

from aiogram.types import Message
from moviepy.video.io.VideoFileClip import VideoFileClip

from app.utils.misc.recognize_audio import get_text_from_audio_file
from settings import TMP_DIR


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

    with concurrent.futures.ThreadPoolExecutor() as pool:
        loop = asyncio.get_running_loop()
        voice_text = await loop.run_in_executor(pool, get_text_from_audio_file, _, path_to_voice_wav)

    await msg_recognize_voice.edit_text(voice_text)
    os.remove(path_to_video_note_mp4)
    os.remove(path_to_voice_wav)


def setup(dp: Dispatcher, *args, **kwargs):
    dp.message.register(
        recognize_video_note, F.chat.type.in_(('supergroup', 'group')), content_types=['video_note']
    )
