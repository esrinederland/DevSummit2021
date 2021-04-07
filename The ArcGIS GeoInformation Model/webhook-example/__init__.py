import logging
import urllib.parse
import os
from . import WebHookExample
import azure.functions as func

__version__ = "v20200824.02"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f'{__version__} Python HTTP trigger function processed a request. WebHookExample2020')
    try:
        bodybytes = req.get_body()
        bodystring = bodybytes.decode('utf-8')
        # logging.info("bodystring: {}".format(bodystring))

        bodyobject = urllib.parse.parse_qs(bodystring)
        logging.info("bodyobject: {}".format(bodyobject))
        logging.info("agolusername: {}".format(os.environ["AGOL_USERNAME"]))
        WebHookExample.ParseBody(bodyobject,os.environ["AGOL_USERNAME"],os.environ["AGOL_PASSWORD"],os.environ["WEBHOOK_TELEGRAM_BOTID"],os.environ["WEBHOOK_TELEGRAM_CHATID"])
        return func.HttpResponse(f"This HTTP triggered function executed successfully. {__version__}")
    except Exception as ex:
        logging.exception("error parsing body")
        return func.HttpResponse(
             f"This HTTP triggered function executed unsuccessfully. v{__version__} Error: {ex}",
             status_code=500
        )
   
       
