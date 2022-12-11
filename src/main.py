from json import loads
from uuid import uuid4
from re import search

from oauth2client.service_account import ServiceAccountCredentials
from discord.ext.commands.context import Context
from discord import PermissionOverwrite
from discord.channel import TextChannel
from discord.message import Message
from discord.guild import Guild
from discord import File
from discord.utils import get
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
import requests

from utils import delete_file
from utils import create_discord_bot
from config import CONFIG
from config import PATH
import twitch



discord = create_discord_bot()
google_drive_service = build(
  'drive', 
  'v3', 
  credentials=ServiceAccountCredentials.from_json_keyfile_dict(loads(CONFIG.GOOGLE_DRIVE_AUTHENTICATION))
)


@discord.event
async def on_guild_join(guild: Guild):
  for guild in discord.guilds:
    channel_names = (
      channel.name
      for channel 
      in guild.channels 
      if isinstance(channel, TextChannel)
    )

    overwrites = {
      guild.default_role: PermissionOverwrite(read_messages=False),
      guild.me: PermissionOverwrite(read_messages=True),
    }
    category = get(guild.categories, name=CONFIG.DISCORD_CATEGORY_NAME)

    if CONFIG.DISCORD_CHANNEL_NAME not in channel_names:
      await guild.create_text_channel(CONFIG.DISCORD_CHANNEL_NAME, overwrites=overwrites, category=category)


@discord.event
async def on_message(message: Message):
  if message.channel.name == CONFIG.DISCORD_CHANNEL_NAME:
    matches = search(r'^https://clips.twitch.tv/(.+)$', message.content)
    if matches:
      slug = matches.group(1)
      await message.channel.send(f'Processing clip: {slug}')

      output_filename = f'{slug}-{uuid4()}.mp4'
      url = twitch.get_download_url(slug)

      with open(output_filename, 'wb') as output:
        output.write(requests.get(url).content)

      file_metadata = {'name': f'{slug}.mp4', 'parents': [CONFIG.GOOGLE_DRIVE_FOLDER_ID]}
      media = MediaFileUpload(output_filename, mimetype='video/mp4')
      file_id = google_drive_service.files().create(
        body=file_metadata, 
        media_body=media, 
        fields='id'
      ).execute()['id']

      await message.channel.send(f'Upload successed! You can access it here: https://drive.google.com/file/d/{file_id}/view')

      discord.loop.run_in_executor(None, lambda: delete_file(output_filename))
  
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
