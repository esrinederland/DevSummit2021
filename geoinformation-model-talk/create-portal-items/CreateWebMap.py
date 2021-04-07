import Security
import requests
import datetime
import json

def main():
    token = Security.GenerateToken()

    print("Getting service info")

    name = "mjagtDemo"

    filePath = r"D:\Demo\newwebmapdata.json"
    newWebMapData = ""
    with open(filePath,"r") as f:
        newWebMapData = f.read() 

    webmapInfo = {}
    webmapInfo["f"] = "json"
    webmapInfo["token"] = token
    webmapInfo["title"] = f"Generated webmap for {name}"
    webmapInfo["tags"] = f"Generated,REST,Demo,{name}"
    webmapInfo["description"] = f"Hello {name}, this is a newly created webmap."
    webmapInfo["type"] = "Web Map"
    webmapInfo["extent"] = "[[1.7692,50.7169],[9.8826,53.5056]]"
    webmapInfo["text"] = newWebMapData

    
    addItemurl = f"https://www.arcgis.com/sharing/rest/content/users/{Security.GetUsername()}/d1514d6b25fa41ceb43a7e2016fead3a/addItem"

    r = requests.post(addItemurl,webmapInfo)
    print(r.text)
    


    print("script complete")


if __name__=="__main__":
    main()
