import logging
import json
import requests
import datetime
import time

def ParseBody(body,agol_usr,agol_pwd,t_botid,t_chatid):
    logging.debug("WebHookExample::ParseBody::Start")
    logging.debug(f"body: {body}")
    if not "payload" in body:
        logging.error("no payload in body")
        return

    payload = json.loads(body["payload"][0])[0]

    #getting token
    token = GenerateToken(agol_usr,agol_pwd)

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
        statusurl = changesResult["statusUrl"]
        logging.debug(f"getting data from statusurl: {statusurl}")
        r = requests.post(statusurl,params)
        logging.debug("Getting result")
        statusResult = r.json()

        status = statusResult['status']
        logging.info(f"status result status: {status}")
        if status != "Completed":
            logging.info("Sleeping for 1s")
            time.sleep(1)
        else:
            resultUrl = statusResult['resultUrl']
        
    if resultUrl:
        logging.info(f"getting data from resulturl: {resultUrl}")
        r = requests.post(resultUrl,params)
        logging.info("Getting result")
        results = r.json()
        logging.info(f"found results: {results}")

        edits = results['edits'][0]
        
        addedFeatures = []
        if "adds" in edits['features']:
            logging.info("Adding adds")
            addedFeatures = addedFeatures + edits['features']['adds']

        if "edits" in edits['features']:
            logging.info("Adding edits")
            addedFeatures = addedFeatures + edits['features']['edits']
        
        logging.info(f"Found {len(addedFeatures)} adds")
        counter =0
        for feature in addedFeatures:
            counter +=1
            logging.info(feature)
            name = GetAttributeValueFuzzy(feature,"name")
            msg = GenerateMessageFromFeature(feature)
            msg += f"{counter}/{len(addedFeatures)}"
            SendTelegramMessage(t_botid,t_chatid,msg)

            logging.info(f"Feature {name} {counter}/{len(addedFeatures)}")

    logging.info("Script complete")

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

def GenerateToken(username, password):
    logging.debug("GenerateToken::Start")
    
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