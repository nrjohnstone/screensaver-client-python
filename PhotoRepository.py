import requests

class PhotoRepository:
    """Client for retrieving images from PhotoService API"""

    def __init__(self, host, port, client_id):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.base_url = "http://" + host + ":" + str(port) + "/api"

    def getPhotoList(self, guid):
        response = requests.get(self.base_url + "/photoLists/" + guid)
        return response

    def createPhotoList(self, guid):
        response = requests.post(self.base_url + "/photoLists/" + guid)
        return response

    def getPhoto(self, image_index):
        image_url = self.base_url + "/" + self.client_id + "/photos/" + str(image_index) + "/data"
        response = requests.get(image_url)
        return response
