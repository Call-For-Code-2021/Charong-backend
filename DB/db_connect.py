from ibmcloudant import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv
import os
#getting dotenv file
load_dotenv(verbose=True)
class Db_coneection():
    authenticator = IAMAuthenticator(os.getenv('IBM_CLOUDANT_API_KEY'))
    service = CloudantV1(authenticator=authenticator)
    def __init__(self):
        self.service.set_service_url(os.getenv('IBM_CLOUDANT_URL'))

    def get_service(self):
        return self.service
