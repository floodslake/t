import os

token = os.getenv("PD_TOKEN")
folder = os.getenv("FOLDER")

for file in sorted(os.listdir(folder)):
  command = f'curl -g -T "{folder}/{file}" -u :{token} https://pixeldrain.com/api/file/'
  os.system(command)
