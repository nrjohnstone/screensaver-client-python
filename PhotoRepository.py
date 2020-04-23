import requests
import io


class PhotoRepository:
    """Client for retrieving images from PhotoService API"""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.base_url = "http://" + host + ":" + str(port) + "/api"

    def getPhotoList(self, guid):
        response = requests.get(self.base_url + "/photoLists/" + guid)

        if response.status_code == 200:
            photo_list_json = response.json()
            return PhotoListResult(photo_list_json['total'],
                                   photo_list_json['currentIndex'],
                                   response.status_code)
        else:
            return PhotoListResult(None, None, response.status_code)

    def createPhotoList(self, guid):
        response = requests.post(self.base_url + "/photoLists/" + guid)
        return CreatePhotoListResult(response.status_code)

    def getPhoto(self, photo_list_id, image_index):
        image_url = self.base_url + "/photolists/" + photo_list_id + "/photos/" + str(image_index) + "/data"
        response = requests.get(image_url)
        image_data = io.BytesIO(response.content)
        return GetPhotoResult(image_data, response)

    def update_current_index(self, photo_list_id, current_index):
        uri = self.base_url + "/photoLists/" + photo_list_id + "/currentIndex"
        content = str(current_index)
        headers = {
            'Content-Type': 'application/json; UTF-8'
        }
        response = requests.put(uri, data=content.encode('utf-8'), headers=headers)
        return response.status_code == 200


class PhotoListResult:

    def __init__(self, total, current_index, status_code):
        self.total = total
        self.current_index = current_index
        self.status_code = status_code


class CreatePhotoListResult:

    def __init__(self, status_code):
        self.status_code = status_code


class GetPhotoResult:

    def __init__(self, image_data, status_code):
        self.status_code = status_code
        self.image_data = image_data
