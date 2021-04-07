import logging
from . import SelfServiceStoryMapping2020
import urllib.parse
import os
import azure.functions as func



__version__ = "v202000901.01"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f'{__version__} Python HTTP trigger function processed a request. SelfServiceStoryMapping2020')
    try:
        bodybytes = req.get_body()
        bodystring = bodybytes.decode('utf-8')
        # logging.info("bodystring: {}".format(bodystring))

        bodyobject = urllib.parse.parse_qs(bodystring)
        logging.info("bodyobject: {}".format(bodyobject))
        logging.info("agolusername: {}".format(os.environ["AGOL_USERNAME"]))
        SelfServiceStoryMapping2020.ParseBody(bodyobject)
        return func.HttpResponse(f"This HTTP triggered function executed successfully. {__version__}")
    except Exception as ex:
        logging.exception("error parsing body")
        return func.HttpResponse(
             f"This HTTP triggered function executed unsuccessfully. v{__version__} Error: {ex}",
             status_code=500
        )
   
       