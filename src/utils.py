from discord.ext.commands.bot import Bot
from discord import Intents 
from os import remove
from os.path import exists
from threading import Timer


def create_discord_bot() -> Bot:
  intents = Intents.default()
  intents.message_content = True
  intents.auto_moderation = True
  return Bot(command_prefix='!', intents=intents)

def delete_file(path: str): 
  try:
    remove(path)
  except PermissionError:
    print(f'Cannot delete {path} is being used by another process.')
  except FileNotFoundError:
    print(f'File {path} already been deleted.')

def delete_file_threaded(path: str):
  Timer(30, lambda: delete_file(path)).start()
