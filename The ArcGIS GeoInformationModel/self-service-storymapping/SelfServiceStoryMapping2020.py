import logging
import os
import json
import requests
import datetime
import copy
import time
import math

_regionServiceLayerUrl = "https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/SelfServiceStoryMapping2020_Regions/FeatureServer/0"
_sssServiceLayerUrl = "https://services.arcgis.com/emS4w7iyWEQiulAb/ArcGIS/rest/services/SelfServiceStoryMapping2020/FeatureServer/0"
_sssPublicServiceLayerUrl = "https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/SelfServiceStoryMapping2020_Public/FeatureServer/0"
_routeToDestinationServiceLayerUrl = "https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/SelfServiceStoryMapping2020_Routes/FeatureServer/0"
_routeEnd = {"x":678156, "y":6891553}
_templateWebMapId = "24b50efa64f949ad92e5a4a2dadd4170"
_resultAGOLFolderID = "cb9640f48dc34c43a5cda587a07e83c4"
_templateStoryMapId = "08ba6bd499c84a5d8eb23aaf266c5bd0"

def main():
    logging.basicConfig(level=logging.DEBUG)
    #serverGens=[46245119,46245124]
    bodyObject = {'payload': ['[{"name":"EGT20_SSS_InputWebhook","layerId":0,"orgId":"emS4w7iyWEQiulAb","serviceName":"SelfServiceStoryMapping2020_Input","lastUpdatedTime":1598384867282,"changesUrl":"https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/SelfServiceStoryMapping2020_Input/FeatureServer/extractChanges?serverGens=[46245100,46245124]&async=true&returnUpdates=false&returnDeletes=false","events":["FeaturesCreated","AttachmentsCreated"]}]']}
    ParseBody(bodyObject)
    tempFeature = {'geometry': {'x': 630067.204695026,'y': 6939551.364641505},'attributes': {'OBJECTID': 29,'GlobalID': 'EC3DDD1C-03A7-4076-B3FA-EA84C74F1294','CreationDate': 1598384913221,'Creator': '','EditDate': 1598384913221,'Editor': '','NAME': 'Maarten van Hulzen','Description': 'Geweldige Sessie','Email': 'mvanhulzen@esri.nl','Username': 'mvanhulzendev','Status': 'New','Provincie': None}}
    GenerateStoryMapForFeature(tempFeature)



def ParseBody(body):
    logging.info("SSS2020::GenerateStorymap::Start")
    logging.info(f"body: {body}")
    featuresChanged = GetFeaturesForPayloadBody(body)

    counter = 0
    for feature in featuresChanged:
        counter +=1
        logging.info(f"Parsing feature {counter}/{len(featuresChanged)}")
        try:
            GenerateStoryMapForFeature(feature)
        except:
            logging.exception(f"Error generating storymap for feature {counter}")
    
    logging.info("Script complete")

def GenerateStoryMapForFeature(feature):
    logging.debug("GenerateStoryMapForFeature::start")

    username = os.environ["AGOL_USERNAME"]
    
    name = feature["attributes"]["NAME"]
    comment = feature["attributes"]["Description"]
    agol_username = feature["attributes"]["Username"]
    email = feature["attributes"]["Email"]
    inputgeometry= feature["geometry"]
    inputOid = feature["attributes"]["OBJECTID"]

    logging.info(f"Parsing feature for name: {name}")
    
    token = GenerateToken()

    # Update Country Count
    region = UpdateCountryCount(inputOid,inputgeometry,token)
    feature["attributes"]["Provincie"] = region
    # Create Route to destination
    routeGeometry,routeLength = GenerateRouteToDestination(inputgeometry,token)
    
    # Insert geometry
    routeoid = InsertRouteGeometry(inputOid,name,routeGeometry,routeLength,token)

    # Get extent from route
    extent = GetExtentFromRoute(routeGeometry)

    # Create Webmap with filters
    newWebMapId = CreateWebMap(inputOid,name,extent,username,token)

    # Create Storymap
    newStoryMapId, newStoryMapUrl = CreateStoryMap(newWebMapId,inputOid,name,comment,region,username,token)

    #create group
    newGroupId = CreateGroup(inputOid,name,token)

    #share items with public and group
    ShareItem(newWebMapId,newGroupId,username,token)
    ShareItem(newStoryMapId,newGroupId,username,token)
    # Share (if username is entered)
    if agol_username is not None and len(agol_username.strip())>0:
        #invite user
        AddUserToGroup(agol_username,newGroupId,token)

    # Email link
    if email is not None and len(email.strip())>0:
        SendEmail(inputOid,email, name, newStoryMapUrl)

    msg = GenerateMessageFromFeature(feature)

    msg += f"{newStoryMapUrl}\r\n"

    SendTelegramMessage(os.environ["WEBHOOK_TELEGRAM_BOTID"],os.environ["WEBHOOK_TELEGRAM_CHATID"],msg)


def GetFeaturesForPayloadBody(body):
    changedFeatures = []
    try:
        if not "payload" in body:
            logging.error("no payload in body")
            
        payload = json.loads(body["payload"][0])[0]

        #getting token
        token = GenerateToken()

        #getting changes response
        
        changesUrl = payload["changesUrl"]
        params = {}
        params["f"] = "json"
        params["token"] = token

        logging.debug(f"getting data from changesurl: {changesUrl}")
        r = requests.post(changesUrl,params)
        logging.debug("Getting result")
        changesResult = r.json()

        status="unknown"
        counter = 0
        resultUrl = None
        
        while status != "Completed" and counter < 10:
            counter+=1
            try:
                statusurl = changesResult["statusUrl"]
                logging.debug(f"getting data from statusurl: {statusurl}")
                r = requests.post(statusurl,params)
                logging.debug("Getting result")
                statusResult = r.json()

                status = statusResult['status']
                logging.info(f"status result status: {status}")
                if status != "Completed":
                    logging.info(f"Sleeping for {counter}")
                    time.sleep(counter)
                    
                else:
                    resultUrl = statusResult['resultUrl']
            except:
                logging.exception("Error getting status of changes")
            
        if resultUrl:
            logging.info(f"getting data from resulturl: {resultUrl}")
            r = requests.post(resultUrl,params)
            logging.info("Getting result")
            results = r.json()
            logging.info(f"found results: {results}")

            edits = results['edits'][0]
            

            if "adds" in edits['features']:
                logging.info("Adding adds")
                changedFeatures = changedFeatures + edits['features']['adds']

            if "edits" in edits['features']:
                logging.info("Adding edits")
                changedFeatures = changedFeatures + edits['features']['edits']

    except Exception as ex:
        logging.exception("Error in GetFeaturesForPayloadBody")
    logging.info(f"Found {len(changedFeatures)} adds")
        
    return changedFeatures

def UpdateCountryCount(featureoid,inputGeometry,token):
    logging.info("UpdateCountryCount::start")

    updateParams = {}
    updateParams["f"] = "json"
    updateParams["token"] = token
    regionName = "Unknown"
    try:
        #get intersecting country
        query = {}
        query["geometryType"] = "esriGeometryPoint"
        query["geometry"]= json.dumps(inputGeometry)
        query["inSR"]= 102100
        query["where"] = "1=1"
        query["outFields"] = "OBJECTID,Name,MEMBER_COUNT"
        query["returnGeometry"] = False
        query["f"] = "json"
        query["token"]= token

        queryUrl = "{}/query".format(_regionServiceLayerUrl)

        queryResult = requests.post(queryUrl,query)

        queryResultObject = queryResult.json()
        logging.debug("Found {} countries".format(len(queryResultObject["features"])))
        if(len(queryResultObject["features"])>0):
        
            feature = queryResultObject["features"][0]
            feature["attributes"]["MEMBER_COUNT"]+=1
            features = []
            features.append(feature)
            regionName = feature["attributes"]["Name"]

            #Update membercount
            updateParams = {}
            updateParams["f"] = "json"
            updateParams["token"] = token
            updateParams["features"] = json.dumps(features)

            updateCountriesUrl = "{}/updateFeatures".format(_regionServiceLayerUrl)

            updateResponse = requests.post(updateCountriesUrl,updateParams)

            logging.info(f"Update countries: {updateResponse.text}")
    except:
        logging.exception("Error updating regioncount")

    #update surveycountry record
    feature = {}
    feature["attributes"] = {}
    feature["attributes"]["OBJECTID"] = featureoid
    feature["attributes"]["Provincie"] = regionName
    feature["attributes"]["Status"] = "Processed"
    features = []
    features.append(feature)
    updateParams["features"] = json.dumps(features)
    
    updateSurveyUrl = "{}/updateFeatures".format(_sssServiceLayerUrl)

    updateResponse = requests.post(updateSurveyUrl,updateParams)

    logging.info(f"Update survey: {updateResponse.text}")

    return regionName

def GenerateRouteToDestination(fromGeometry, token):
    logging.info("GenerateRouteToDestination::start")
    routeGeometry = None
    
    #create a simple geometry (straight line) and a dummy length
    startVertice = [fromGeometry["x"],fromGeometry["y"]]
    endVertice = [_routeEnd["x"],_routeEnd["y"]]
    singlePath = []
    singlePath.append(startVertice)
    singlePath.append(endVertice)
    routeGeometry = {}
    routeGeometry["paths"] = [singlePath]
    routeGeometry["spatialReference"] = {"wkid": "102100"}
    routeLength = 42
    
    if True:

        # URL TO THE ESRI WORLD ROUTING SERVICE
        routingUrl = "https://route.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve"
        fromFeature = {"geometry":fromGeometry}
        fromFeature["geometry"]["spatialReference"] = {"wkid": "102100"}
        toFeature = {"geometry": {"x": _routeEnd["x"], "y": _routeEnd["y"], "spatialReference": {"wkid": "102100"}}, "attributes": {"Name": "To Location"}}
        stops = [fromFeature, toFeature]
        routingParams = {
            "f": "json",
            "stops": '{{"type":"features","features": {}}}'.format(stops),
            "token": token,
            "outSR":4326
        }

        r = requests.post(routingUrl, routingParams)
        route = r.json()

        #check if there are valid results
        if "routes" in route and "features" in route["routes"] and len(route["routes"]["features"])>0:
            #print(route)
            routeGeometry = route["routes"]["features"][0]["geometry"] 
            routeGeometry["spatialReference"] = {"wkid": "4326"}
            routeLength = route["routes"]["features"][0]["attributes"]["Total_Kilometers"]
            routeLength = round(routeLength,1)

    return routeGeometry,routeLength

def InsertRouteGeometry(parentoid,name,routeGeometry,routeLength,token):
    logging.info("InsertRouteGeometry::start")
    features = []

    feature = {}
    feature["attributes"] = {}
    feature["attributes"]["NAME"] = name
    feature["attributes"]["PARENT_OID"] = parentoid
    feature["attributes"]["LENGTH"] = routeLength
    feature["geometry"] = routeGeometry
    features.append(feature)

    logging.info("sending request")
    addFeatureUrl = "{}/AddFeatures".format(_routeToDestinationServiceLayerUrl)
    params = {'features':json.dumps(features),'f':'json',"token":token}
        
    r = requests.post(addFeatureUrl,params)

    logging.info(r.text)

def GetExtentFromRoute(routeGeometry):
    if not "spatialReference" in routeGeometry or routeGeometry["spatialReference"] is None or routeGeometry["spatialReference"]["wkid"] != "4326":
        return None
    
    xmin = str(math.floor(min([coords[0] for coords in routeGeometry["paths"][0]])*100)/100.0)
    xmax = str(math.ceil(max([coords[0] for coords in routeGeometry["paths"][0]])*100)/100.0)
    ymin = str(math.floor(min([coords[1] for coords in routeGeometry["paths"][0]])*100)/100.0)
    ymax = str(math.ceil(max([coords[1] for coords in routeGeometry["paths"][0]])*100)/100.0)

    return [xmin,ymin,xmax,ymax]


def CreateWebMap(inputoid,name,newextent,origin_username,token):
    logging.info("Creating webmap")
    defaultParams = {"f":"json","token":token}

    templateItemInfoUrl = f"https://www.arcgis.com/sharing/rest/content/items/{_templateWebMapId}"
    # r = requests.get(templateItemInfoUrl,defaultParams)
    # templateItemInfo = r.json()

    templateItemDataUrl = f"{templateItemInfoUrl}/data"
    r = requests.get(templateItemDataUrl,defaultParams)
    templateItemData = r.json()

    logging.info(f"Creating webmap for {name}")

    newWebmapData = copy.deepcopy(templateItemData)
    pointLayers = [layer for layer in newWebmapData["operationalLayers"] if layer["title"]=="POINTS"]
    if len(pointLayers)>0:
        pointLayer = pointLayers[0]
        if not "layerDefinition" in pointLayer:
            pointLayer["layerDefinition"] = {}
        pointLayer["layerDefinition"]["definitionExpression"] = f"objectid={inputoid}"

    routeLayers = [layer for layer in newWebmapData["operationalLayers"] if layer["title"]=="ROUTES"]
    if len(routeLayers)>0:
        routeLayer = routeLayers[0]
        if not "layerDefinition" in routeLayer:
            routeLayer["layerDefinition"] = {}
        routeLayer["layerDefinition"]["definitionExpression"] = f"PARENT_OID={inputoid}"
  
    webmapInfo = defaultParams.copy()
    webmapInfo["title"] = f"SSS20 {inputoid} Generated webmap for {name}"
    webmapInfo["tags"] = f"EGT20,DevDay,DevDay2020,REST,Demo,{name},EGT20RESTSSS,SSS"
    webmapInfo["description"] = f"Hello {name}, this is a newly created webmap."
    webmapInfo["type"] = "Web Map"
    webmapInfo["text"] = json.dumps(newWebmapData)
    
    if newextent is not None:
        webmapInfo["extent"] = ",".join(newextent)

    addItemurl = f"https://www.arcgis.com/sharing/rest/content/users/{origin_username}/{_resultAGOLFolderID}/addItem"

    r = requests.post(addItemurl,webmapInfo)
    logging.debug(r.text)
    
    newWebMapId = r.json()["id"]
    return newWebMapId

def CreateStoryMap(newWebMapId,inputoid,name,comment,region,origin_username,token):
    logging.info("CreateStoryMap::start")
    defaultParams = {"f":"json","token":token}
    
    templateItemInfoUrl = f"https://www.arcgis.com/sharing/rest/content/items/{_templateStoryMapId}"
    r = requests.get(templateItemInfoUrl,defaultParams)
    templateItemInfo = r.json()

    templateItemDataUrl = f"{templateItemInfoUrl}/data"
    r = requests.get(templateItemDataUrl,defaultParams)
    templateItemData = r.json()

    logging.info(f"Creating storymap for {name}")

    newItemData = copy.deepcopy(templateItemData)
   
    #determine image url (if it is there)
    attachmentInfosUrl = f"{_sssPublicServiceLayerUrl}/{inputoid}/attachments"
    r = requests.post(attachmentInfosUrl,defaultParams)
    attachmentInfos = r.json()
    
    #if there are attachments
    if len(attachmentInfos["attachmentInfos"])>0:
        attachmentid = attachmentInfos["attachmentInfos"][0]["id"]
        attachmentImageUrl = f"{attachmentInfosUrl}/{attachmentid}"
        
        #find the first image resource and replace it
        for itemkey in newItemData["resources"].keys():
            if newItemData["resources"][itemkey]["type"]=="image":
                logging.debug(f"Setting resourceid of {itemkey} to {attachmentImageUrl}")
                newItemData["resources"][itemkey]["data"]["resourceId"] = attachmentImageUrl
                break

    newItemDataText = json.dumps(newItemData)
    newItemDataText = newItemDataText.replace("{name}",name)
    newItemDataText = newItemDataText.replace("{comment}",comment)
    newItemDataText = newItemDataText.replace("{region}",region)
    newItemDataText = newItemDataText.replace(_templateWebMapId,newWebMapId)

    newItemInfo = defaultParams.copy()
    newItemInfo["title"] = f"SSS {inputoid} Generated storymap for {name}"
    newItemInfo["tags"] = f"EGT20,DevDay,DevDay2020,REST,Demo,{name},EGT20RESTSSS,SSS"
    newItemInfo["description"] = f"Hello {name}, this is a newly created storymap."
    newItemInfo["type"] = "StoryMap"
    newItemInfo["typeKeywords"] = ",".join(templateItemInfo["typeKeywords"])
    newItemInfo["text"] = newItemDataText

    addItemurl = f"https://www.arcgis.com/sharing/rest/content/users/{origin_username}/{_resultAGOLFolderID}/addItem"

    r = requests.post(addItemurl,newItemInfo)
    logging.debug(r.text)

    newItemId = r.json()["id"]

    #update the url property to open in properly in arcgis online
    newUrl = f"https://storymaps.arcgis.com/stories/{newItemId}"

    updateUrl = f"https://www.arcgis.com/sharing/rest/content/users/{origin_username}/{_resultAGOLFolderID}/items/{newItemId}/update"
    updateParams = defaultParams.copy()
    updateParams["url"] = newUrl
    r = requests.post(updateUrl,updateParams)
    logging.debug(r.text)

    return newItemId, newUrl

def CreateGroup(inputoid, name,token):
    logging.info("CreateGroup::start")
    newGroupName = f"SSS20 {inputoid} {name}"
   
    newGroupDesc = f"Group for Self Service Storymapping demo for {name} (surveyid: {inputoid})"
    newGroupParams = {'title':newGroupName,'access':'private','description':newGroupDesc, "isViewOnly":True,"isInvitationOnly":True,"tags":f"EGT20,DevDay,DevDay2020,REST,Demo,{name},EGT20RESTSSS,SSS"}

    url='https://www.arcgis.com/sharing/rest/community/createGroup?f=json&token={}'.format(token)

    ### SEND THE REQUEST TO CREATE THE GROUP
    logging.debug("Sending request")
    r = requests.post(url,newGroupParams)
    logging.debug(r.text)
    result = r.json()

    groupid = result["group"]["id"]

    return groupid

def ShareItem(itemid, groupid, origin_username, token):
    logging.info("ShareItem::start")
    url = f"https://www.arcgis.com//sharing/rest/content/users/{origin_username}/items/{itemid}/share"
    groupParam = {'everyone':True,'org':False,'groups':groupid,"f":"json","token":token}

    r = requests.post(url,groupParam)
    logging.debug(r.text)

def AddUserToGroup(agol_username,newGroupId,token):
    logging.info("AddUserToGroup::start")
    url = f"https://www.arcgis.com/sharing/rest/community/groups/{newGroupId}/invite"
    groupParam = {'users':agol_username,"f":"json","token":token}

    r = requests.post(url,groupParam)
    logging.debug(r.text)

def SendEmail(inputoid,email, name, newStoryMapUrl):
    logging.info("SendEmail::start")
    
    params = {"inputoid":inputoid,"email":email,"name":name,"newStoryMapUrl":newStoryMapUrl}
    r = requests.post(os.environ["POWERAUTOMATE_URL"],json=params)
    logging.debug(r.text)

def GenerateToken():
    logging.debug("GenerateToken::Start")
    username = os.environ["AGOL_USERNAME"]
    password = os.environ["AGOL_PASSWORD"]
    # Get token
    token_URL = 'https://www.arcgis.com/sharing/generateToken'
    token_params = {'username':username,'password':password,'referer': "https://www.arcgis.com",'f':'json','expiration':60}
    
    r = requests.post(token_URL,token_params)
    token_obj= r.json()
    
    token = token_obj['token']
    expires = token_obj['expires']

    tokenExpires = datetime.datetime.fromtimestamp(int(expires)/1000)

    logging.debug("new token: {}".format(token))
    logging.info("token for {} expires: {}".format(username,tokenExpires))
    return token   


def GetAttributeValueFuzzy(feature,fieldnamepart):
    fieldName = GetAttributeNameFuzzy(feature,fieldnamepart)
    if fieldName is not None:
        return feature["attributes"][fieldName]
    else:
        return None

def GetAttributeNameFuzzy(feature,fieldnamepart):
    fieldNames = [f for f in feature["attributes"].keys() if f.upper().startswith(fieldnamepart.upper())]
    if len(fieldNames) >0:
        return fieldNames[0]
    else:
        return None

def GenerateMessageFromFeature(feature):
    atts = feature["attributes"]
    nameField = GetAttributeNameFuzzy(feature,"name")
    descField = GetAttributeNameFuzzy(feature,"description")
    datestampField = GetAttributeNameFuzzy(feature,"EditDate")

    usedAttributes = []
    msg = ""
    if nameField is not None:
        msg += f"Name: {atts[nameField]}\r\n"
        usedAttributes.append(nameField)
    if descField is not None:
        msg += f"Desc: {atts[descField]}\r\n"
        usedAttributes.append(datestampField)
    if datestampField is not None:
        datestring = datetime.datetime.fromtimestamp(atts[datestampField]/1000).strftime("%Y%m%d-%H:%M:%S")
        msg += f"Date: {datestring}\r\n"
        usedAttributes.append(datestampField)
    
    remainingFields = [field for field in feature["attributes"].keys() if field not in usedAttributes]
    
  
    for key in remainingFields:
        msg += f"{key} : {feature['attributes'][key]} \r\n" 
    msg += "---\r\n"

    return msg

def SendTelegramMessage(botid, chatid, message):
    telegramURL = "https://api.telegram.org/bot" + botid + "/sendMessage"
    params = {'text': message, 'chat_id': chatid, 'parse_mode': 'HTML'}

    r = requests.post(telegramURL,params)

    print(r.text)


if __name__ == "__main__":
    main()