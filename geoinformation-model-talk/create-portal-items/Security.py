#-------------------------------------------------------------------------------
# Name:        Security 
# Purpose:     Uses the OS Keystore to store password
#              Use "pip install keyring" to use this module
# Author:      mvanhulzen
#
# Created:     21081120
# Copyright:   (c) Esri Nederland 2018
# Licence:     MIT License
#-------------------------------------------------------------------------------


import keyring
import sys
import logging
import requests
import datetime
import socket

_systemname = "Arcgis.com"
if socket.getfqdn()=="ESRIBX0560.esrinl.com":
    _username = "mvanhulzen_esrinl"
elif socket.getfqdn()=="ESRIBX0755.esrinl.com":
    _username="mjagtDemo"

_log = logging.getLogger()

def GetUsername():
    _log.info("Security::GetUsername::start")
    return _username


def GetPassword():
    pwd = keyring.get_password(_systemname, _username)
    if pwd is None:
        _log.info("No password set for {}: {}".format(_systemname, _username))  
    return pwd

def SetPassword(new_password):
    keyring.set_password(_systemname, _username, new_password)
    _log.info("new password set to: {}".format(new_password))

def main():
    logging.basicConfig(level=logging.DEBUG)
    _log.info("Type a (new) password for {}/{}, or press ctrl+c to cancel:".format(_systemname,_username))
    input_func = input
    if sys.version_info < (3,0):
        input_func = raw_input
    newpwd =input_func("New password:").strip()
    
    SetPassword(newpwd)

    print("script complete")   


def GenerateToken():
    _log.debug("GenerateToken::Start")
    
    # Get token
    token_URL = 'https://www.arcgis.com/sharing/generateToken'
    token_params = {'username':GetUsername(),'password':GetPassword(),'referer': "https://www.arcgis.com",'f':'json','expiration':60}
    
    r = requests.post(token_URL,token_params)
    token_obj= r.json()
    
    token = token_obj['token']
    expires = token_obj['expires']

    tokenExpires = datetime.datetime.fromtimestamp(int(expires)/1000)

    _log.debug("new token: {}".format(token))
    _log.info("token for {} expires: {}".format(GetUsername(),tokenExpires))
    return token

if __name__ == "__main__":
    main()
