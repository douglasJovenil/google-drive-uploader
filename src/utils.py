from discord.ext.commands.bot import Bot
from discord import Intents 
from os import remove
from os.path import exists



def create_discord_bot() -> Bot:
  intents = Intents.default()
  intents.message_content = True
  intents.auto_moderation = True
  return Bot(command_prefix='!', intents=intents)


def delete_file(path: str):
  while exists(path):
    try:
      remove(path)
    except PermissionError:
      print(f'Cannot delete {path} is being used by another process.')
    except FileNotFoundError:
      print(f'File {path} already been deleted.')
