from ibmcloudant import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class Db_coneection():
    authenticator = IAMAuthenticator('HYt6CLoiZqQvFWzWJ6qV72WedUz9uQDrmTsTiGr55rcs')
    service = CloudantV1(authenticator=authenticator)
    def __init__(self):
        self.service.set_service_url('https://apikey-v2-31klrndh0xoyzm3uu9k25en7hy1etfdp59c6hvp1vspu:6d9976cf244d2e8566f90da6a0e24037@507f66e8-43f9-4898-ad08-24afea16c7c1-bluemix.cloudantnosqldb.appdomain.cloud')

    def get_service(self):
        return self.service
