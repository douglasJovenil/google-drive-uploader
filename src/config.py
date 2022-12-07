from environ import config
from environ import var


@config
class Config:
  DISCORD_TOKEN: str = var()
  DISCORD_CATEGORY_NAME: str = var()
  DISCORD_CHANNEL_NAME: str = var(converter=lambda name: name.lower())
  TWITCH_CLIENT_ID: str = var()
  GOOGLE_DRIVE_AUTHENTICATION: str = var()
  GOOGLE_CLIENT_SECRETS_FILENAME: str = var(default='client_secrets.json')
  GOOGLE_DRIVE_FOLDER_ID: str = var()

  @property
  def GOOGLE_DRIVE_CURRENT_FOLDER_URL(self) -> str:
    return f'https://drive.google.com/drive/folders/{self.GOOGLE_DRIVE_FOLDER_ID}'

CONFIG: Config = Config.from_environ() # type: ignore
