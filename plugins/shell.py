# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message
from config import Config
import subprocess
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

@Client.on_message(filters.command(Config.SHELL_COMMAND))
async def shell(client: Client, message: Message):
    if Config.OWNER_ID == 0: LOGGER.warning("owner id was 0. shell cannot run.")
    if not (Config.OWNER_ID != 0 and message.from_user.id == Config.OWNER_ID): return
    try:
        cmd = message.text.split(' ', 1)
        if len(cmd) == 1:
            await message.reply_text('🇬🇧 No command to execute was given.\n🇹🇷 Boşluk bırakıp komut gir zırcahil seni.',
                reply_to_message_id = message.message_id)
            return
        cmd = cmd[1]
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        reply = ''
        stderr = stderr.decode()
        stdout = stdout.decode()
        if stdout:
            reply += f"Stdout:\n`{stdout}`\n"
            LOGGER.info(f"Shell - {cmd} - {stdout}")
        if stderr:
            reply += f"Stderr:\n`{stderr}`\n"
            LOGGER.error(f"Shell - {cmd} - {stderr}")
        if len(reply) > 3000:
            with open('shell.txt', 'w') as file:
                file.write(reply)
            with open('shell.txt', 'rb') as doc:
                await client.send_document(
                    document=doc,
                    file_name =doc.name,
                    reply_to_message_id=message.message_id,
                    chat_id=message.chat.id)
        else:
            await message.reply_text(reply)
    except:
        await message.reply_text("🇬🇧 Maybe your shell message was empty.\n🇹🇷 Boş bir şeyler döndü valla.",
            reply_to_message_id = message.message_id)