from config import CONFIG
from urllib import parse
import requests


class ConsoleError(Exception):
  """Raised when an error occurs and script exectuion should halt."""
  pass


class GQLError(Exception):
  def __init__(self, errors):
    super().__init__("GraphQL query failed")
    self.errors = errors


def authenticated_post(url, data=None, json=None, headers={}):
  headers['Client-ID'] = CONFIG.TWITCH_CLIENT_ID

  response = requests.post(url, data=data, json=json, headers=headers)
  if response.status_code == 400:
    data = response.json()
    raise ConsoleError(data["message"])

  response.raise_for_status()

  return response


def gql_post(query):
  url = "https://gql.twitch.tv/gql"
  response = authenticated_post(url, data=query).json()

  if "errors" in response:
    raise GQLError(response["errors"])

  return response


def get_clip_access_token(slug):
  query = """
  {{
    "operationName": "VideoAccessToken_Clip",
    "variables": {{
      "slug": "{slug}"
    }},
    "extensions": {{
      "persistedQuery": {{
        "version": 1,
        "sha256Hash": "36b89d2507fce29e5ca551df756d27c1cfe079e2609642b4390aa4c35796eb11"
      }}
    }}
  }}
  """

  response = gql_post(query.format(slug=slug).strip())
  return response["data"]["clip"]


def get_download_url(slug: str) -> str:
  clip_data = get_clip_access_token(slug)
  source_url = clip_data['videoQualities'][0]['sourceURL']
  query_params = parse.urlencode({
    'sig': clip_data['playbackAccessToken']['signature'],
    'token': clip_data['playbackAccessToken']['value'],
  })
  return f'{source_url}?{query_params}'
