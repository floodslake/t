import requests
import time

while True:
    try:
        getServer = requests.get("https://api.gofile.io/servers").json()
        
        if getServer['status']=="ok":
            
            try:
                server = getServer['data']['servers'][0]['name']
            except KeyError:
                server = getServer['data']['server']
                
            if server!="store10":
                print(server)
                break
            else:
                time.sleep(15)
                
        else:
            time.sleep(15)
            
    except requests.exceptions.RequestException as e:
        time.sleep(30)
