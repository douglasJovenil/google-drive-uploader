from threading import Timer
from re import search
from os import remove

from discord.ext.commands.context import Context
from discord.ext.commands.bot import Bot
from discord import PermissionOverwrite
from discord.channel import TextChannel
from discord.message import Message
from discord import Intents 
from discord import File
from discord.utils import get
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
import requests

from utils import open_file
from config import CONFIG
from config import PATH
import twitch



intents = Intents.default()
intents.message_content = True
discord = Bot(command_prefix='!', intents=intents)



@discord.event
async def on_guild_join(_):
  with open_file(f'{PATH.SOURCE}/{CONFIG.GOOGLE_CLIENT_SECRETS_FILENAME}') as file:
    file.write(repr(CONFIG.GOOGLE_DRIVE_AUTHENTICATION)[1:-1])

  for guild in discord.guilds:
    channel_names = [
      channel.name
      for channel 
      in guild.channels 
      if isinstance(channel, TextChannel)
    ]

    if CONFIG.DISCORD_CHANNEL_NAME not in channel_names:
      overwrites = {
        guild.default_role: PermissionOverwrite(read_messages=False),
        guild.me: PermissionOverwrite(read_messages=True),
      }
      category = get(guild.categories, name=CONFIG.DISCORD_CATEGORY_NAME)
      await guild.create_text_channel(CONFIG.DISCORD_CHANNEL_NAME, overwrites=overwrites, category=category)


@discord.event
async def on_message(message: Message):
  if message.channel.name == CONFIG.DISCORD_CHANNEL_NAME:
    matches = search(r'^https://clips.twitch.tv/(.+)$', message.content)
    if matches:
      slug = matches.group(1)
      await message.channel.send(f'Processing clip: {slug}')

      output_filename = f'{slug}.mp4'
      url = twitch.get_download_url(slug)
      video = requests.get(url).content
      creds = ServiceAccountCredentials.from_json_keyfile_name(f'{PATH.SOURCE}/{CONFIG.GOOGLE_CLIENT_SECRETS_FILENAME}', ['https://www.googleapis.com/auth/drive.file'])
      service = build('drive', 'v3', credentials=creds)

      with open(output_filename, 'wb') as output:
        output.write(video)
        file_metadata = {'name': output_filename, 'parents': [CONFIG.GOOGLE_DRIVE_FOLDER_ID]}
        media = MediaFileUpload(output_filename, mimetype='video/mp4')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

      await message.channel.send(f'Upload successed! You can access it here: https://drive.google.com/file/d/{file["id"]}/view')
      Timer(1, lambda: remove(output_filename)).start()

  await discord.process_commands(message)


@discord.command(help='Never run this command, it can cause emotional damage!!!')
async def jovenil(ctx: Context):
  await ctx.send(file=File(f'{PATH.RESOURCES}/easter_egg.mp3'))


@discord.command(help='Shows the current folder ID of Google Drive')
async def current(ctx: Context):
  await ctx.send(f'Your current folder is: {CONFIG.GOOGLE_DRIVE_CURRENT_FOLDER_URL}')


@discord.command(
  help='Updates the folder ID to save the files in Google Drive.',
  description='''You can get the ID accessing the folder using your browser and get it from the URL.

  For example in this URL:
    https://drive.google.com/drive/folders/1abcnNaaaa8PgzH_PMSioykbbbqF
    
  The ID is:
    1abcnNaaaa8PgzH_PMSioykbbbqF'''
)
async def update(ctx: Context):
  folder_id = ctx.message.content.replace('!update', '').strip()
  CONFIG.GOOGLE_DRIVE_FOLDER_ID = folder_id
  await ctx.send(f'Folder updated with Success! You can access it here: {CONFIG.GOOGLE_DRIVE_CURRENT_FOLDER_URL}')


if __name__ == '__main__':
  discord.run(CONFIG.DISCORD_TOKEN)
