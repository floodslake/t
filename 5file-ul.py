import json
import requests
import time
import os

folder = os.getenv("FOLDER")
userToken = os.getenv("GO_TOKEN")
parentFolderId = os.getenv("GO_FOLDER")

def createFolder(userToken,parentFolderId):
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ userToken,
  }
  
  json_data = {
    'parentFolderId': parentFolderId,
  }
  
  public_json_data = {
    'attribute': 'public',
    'attributeValue': 'true',
  }
  
  while True:
    createFolder = requests.post('https://api.gofile.io/contents/createFolder', headers=headers, json=json_data).json()
    if createFolder['status']=="ok":
      folderId = createFolder['data']['id']
      code = createFolder['data']['code']
      print(f"New Folder {code}:{folderId} is created")
      break
    else:
      print(createFolder)
      time.sleep(2)
      
  while True:
    public_true = requests.put(f"https://api.gofile.io/contents/{folderId}/update", headers=headers, json=public_json_data).json()
    if public_true['status']=="ok":
      print(f"Folder {code} is public")
      break
    else:
      print(public_true)
      time.sleep(2)
      
  return createFolder['data']
    
  
def getServer():
  while True:
    try:
        getServer = requests.get("https://api.gofile.io/servers", timeout=60).json()
    except requests.exceptions.Timeout:
        server = "store5"
        break
    if getServer['status']=="ok":
      try:
        server = getServer['data']['servers'][0]['name']
      except KeyError:
        server = getServer['data']['server']
      if server!="store10":
        break
      else:
        time.sleep(15)
    else:
     time.sleep(15)
  print(server)
  return server
  
folderData = createFolder(userToken,parentFolderId)
folderId = folderData['id']
code = folderData['code']

for file in sorted(os.listdir(folder)):
  server = getServer()
  ul_command = f'curl -F "token={userToken}" -F "folderId={folderId}" -F "file=@{folder}/{file}" https://{server}.gofile.io/contents/uploadFile'
  print(f"https://gofile.io/d/{code}")
  os.system(ul_command)
  print_cmd = f'echo https://gofile.io/d/{code} >> "output/link.txt"'
  os.system(print_cmd)
