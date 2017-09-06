import requests

def bots_update():
  r = requests.get('https://mixed-connection.herokuapp.com/bots', auth=('user', 'pass'))
  r.status_code
  print (r.status_code)

bots_update()
