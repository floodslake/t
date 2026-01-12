import json
import requests
import time
import os

folder = os.getenv("FOLDER")
userToken = os.getenv("GO_TOKEN")
parentFolderId = os.getenv("GO_FOLDER")
TempFolderId = os.getenv("GO_FOLDER_TEMP")

def createFolder(userToken, parentFolderId):
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ userToken,
  }
  json_data = {
    'parentFolderId': parentFolderId,
    'public': True,
  }
  
  max_retries = 10
  attempts = 0
  while attempts < max_retries:
    try:
      response = requests.post('https://api.gofile.io/contents/createFolder', headers=headers, json=json_data)
      response.raise_for_status()# This checks if the HTTP status is 200, 404, 500, etc.
      result = response.json()
      print(f"Attempt {attempts + 1}: {result.get('status')}")
      if result.get('status') == "ok":
        return result['data']['id'], result['data']['code']
      print(f"API Error: {result}")# If status is not "ok", wait and try again
    except requests.exceptions.RequestException as e:
      print(f"Network/HTTP Error: {e}")
    attempts += 1
    if attempts < max_retries:
      print("Retrying in 30 seconds...")
      time.sleep(5)
  
  return None, None # Return None or raise an error if all attempts fail
    
try:
  folderId, code = createFolder(userToken,parentFolderId)
  for file in sorted(os.listdir(folder)):
    ul_command = f'curl -F "token={userToken}" -F "folderId={folderId}" -F "file=@{folder}/{file}" https://upload.gofile.io/contents/uploadFile'
    print(f"https://gofile.io/d/{code}")
    os.system(ul_command)
    print_cmd = f'echo https://gofile.io/d/{code} >> "output/link.txt"'
    os.system(print_cmd)
except:
  for file in sorted(os.listdir(folder)):
    ul_command = f'curl -F "token={userToken}" -F "folderId={TempFolderId}" -F "file=@{folder}/{file}" https://upload.gofile.io/contents/uploadFile >> "output/link.txt"'
    os.system(ul_command)
