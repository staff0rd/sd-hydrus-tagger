import json
from urllib.parse import quote

import requests
from PIL import Image

from . import constants


# https://hydrusnetwork.github.io/hydrus/developer_api.html
class HydrusApi:
    def __init__(self, host, access_key):
        self.host = host
        self.access_key = access_key

    def request_permissions(self, basic_permissions):
        url = f"{self.host}/request_new_permissions?name={quote(constants.APP_NAME)}&basic_permissions={json.dumps(basic_permissions)}"
        return self.get(url)

    def get_image(self, file_id):
        url = f"{self.host}/get_files/file?file_id={file_id}"

        return Image.open(
            requests.get(
                url,
                stream=True,
                headers={"Hydrus-Client-API-Access-Key": self.access_key},
            ).raw
        )

    def get(self, url):
        result = requests.get(
            url,
            headers={"Hydrus-Client-API-Access-Key": self.access_key},
        )
        if result.status_code != 200:
            raise Exception(f"{url} request failed: {result.text}")
        return result.json()

    def post(self, url, data):
        result = requests.post(
            f"{self.host}{url}",
            json=data,
            headers={"Hydrus-Client-API-Access-Key": self.access_key},
        )
        if result.status_code != 200:
            raise Exception(f"{url} request failed: {result.text}")

    def get_files_to_process(self, extra_tags, force=False):
        tags = []
        if extra_tags is not None:
            tags = extra_tags
        tags_to_process = ["system:has human-readable embedded metadata", *tags]
        if not force:
            tags_to_process.append(constants.PENDING_TAG)
        url = f"{self.host}/get_files/search_files?tags={quote(json.dumps(tags_to_process))}"
        return self.get(url)["file_ids"]

    def get_tag_service_key(self, tag_service_name="my tags"):
        services = self.get(f"{self.host}/get_services")
        local_tags = services["local_tags"]
        for x in local_tags:
            if x["name"] == tag_service_name:
                return x["service_key"]

    def add_tags(self, file_id, service_key, tags):
        url = "/add_tags/add_tags"
        data = {
            "file_id": file_id,
            "service_keys_to_actions_to_tags": {
                f"{service_key}": {
                    "0": [*tags, constants.ALL_TAG, constants.PROCESSED_TAG],
                    "1": [constants.PENDING_TAG],
                }
            },
        }
        result = self.post(url, data)
