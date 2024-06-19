import request
import time

while True:
  getServer = requests.get("https://api.gofile.io/getServer").json()
  if getServer['status']=="ok":
      try:
          server = getServer['data']['servers'][0]['name']
      except KeyError:
          server = getServer['data']['server']
      if server!="store10":
          break
      else:
          print(server)
          time.sleep(2)
