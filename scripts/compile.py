from pathlib import Path
from os import system
from os import popen



def main():
  ROOT_DIR = str(Path(__file__).resolve().parent.parent).replace('\\', '/')
  FILE_NAME = 'google-drive-uploader'
  VENV_DIR = popen('pipenv --venv').read().strip()
  SITE_PACKAGES = f'{VENV_DIR}/Lib/site-packages'

  params = {
    'distpath': f'{ROOT_DIR}/build',
    'workpath': f'{ROOT_DIR}/tmp',
    'specpath': f'{ROOT_DIR}/tmp',
    'noconfirm': '',
    'clean': '',
    'name': f'{FILE_NAME}',
    'add-data': [
      f'{ROOT_DIR}/resources;resources'
    ],
    'paths': [
      f'{ROOT_DIR}/src'
    ]
  }


  cmd = f'pyinstaller {ROOT_DIR}/src/main.py --paths {SITE_PACKAGES}'
  for key, value in params.items():
    if isinstance(value, list):
      cmd += ''.join(f' --{key} {sub_value}' for sub_value in value)
    else:
      cmd += f' --{key} {value}'


  system(cmd)

if __name__ == '__main__':
  main()
