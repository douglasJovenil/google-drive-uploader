from inspect import getmembers
from inspect import isroutine
from pathlib import Path

from akeyless import GetSecretValue
from akeyless import Configuration
from akeyless import ApiClient
from akeyless import V2Api
from akeyless import Auth
from environ import config
from environ import var


@config
class Akeyless:
  AKEYLESS_CLIENT_ID: str = var()
  AKEYLESS_ACCESS_KEY: str = var()

class Config:
  # All this keys are acquired from Akeyless
  # In the Akeyless platform they start with prefix "APP_"
  DISCORD_TOKEN: str
  DISCORD_CATEGORY_NAME: str
  DISCORD_CHANNEL_NAME: str
  TWITCH_CLIENT_ID: str
  GOOGLE_DRIVE_AUTHENTICATION: str
  GOOGLE_DRIVE_FOLDER_ID: str
  GOOGLE_CLIENT_SECRETS_FILENAME: str

  @property
  def GOOGLE_DRIVE_CURRENT_FOLDER_URL(self) -> str:
    return f'https://drive.google.com/drive/folders/{self.GOOGLE_DRIVE_FOLDER_ID}'

  def __init__(self):
    AKEYLESS: Akeyless = Akeyless.from_environ()
    members = getmembers(self, lambda attr: not(isroutine(attr)))
    attrs_as_dict: dict = members[0][1]
    attrs = [ f'APP_{key}' for key in attrs_as_dict.keys() ]

    configuration = Configuration(host='https://api.akeyless.io')
    api_client = ApiClient(configuration)
    api = V2Api(api_client)

    body = Auth(access_id=AKEYLESS.AKEYLESS_CLIENT_ID, access_key=AKEYLESS.AKEYLESS_ACCESS_KEY)
    token = api.auth(body).token
    body = GetSecretValue(names=attrs, token=token)
    secrets = api.get_secret_value(body)

    for key, value in secrets.items():
      attr = key.replace('APP_', '')
      setattr(self, attr, value)

class PATH:
  ROOT = Path(__file__).resolve().parent.parent
  SOURCE = f'{ROOT}/src'
  RESOURCES = f'{ROOT}/resources'


CONFIG = Config() # type: ignore
