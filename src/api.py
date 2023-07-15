import json
from urllib.parse import quote

import requests
from loguru import logger
from PIL import Image


class HydrusApi:
    def __init__(self, host, access_key, pending_tag):
        self.host = host
        self.access_key = access_key
        self.pending_tag = pending_tag

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

    def get_files_to_process(self, extra_tags=[]):
        tags = quote(
            json.dumps(["system:has human-readable embedded metadata", *extra_tags])
        )
        url = f"{self.host}/get_files/search_files?tags={tags}"
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
                    "0": [*tags, "processed-by-tag-editor"],
                    "1": self.pending_tag,
                }
            },
        }
        result = self.post(url, data)
