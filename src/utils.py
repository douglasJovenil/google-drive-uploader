from contextlib import contextmanager


@contextmanager
def open_file(filename):
  with open(filename, 'w'): 
    ...

  try:
    file = open(filename, 'r+')
  except Exception as e:
    print(e)
  else:
    yield file

  finally:
    file.close()
