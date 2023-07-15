from loguru import logger
from tqdm import tqdm

from src.api import HydrusApi
from src.utils import get_comfyui_tags

host = "http://192.168.2.7:45869"
access_key = "a0f7783ba9e550d5f2ef02478a56ef3f27ef0c1d3ebb28aa35038e371f5884ae"

api = HydrusApi(host, access_key, "pending-auto-tagger")
file_ids = api.get_files_to_process(extra_tags=["comfyui"])
service_key = api.get_tag_service_key()
if service_key is None:
    raise Exception("No tag service found")

logger.info(f"Found {len(file_ids)} images to process")

print("Processing images...")

for file_id in tqdm(file_ids):
    image = api.get_image(file_id)
    tags = get_comfyui_tags(image)
    api.add_tags(file_id, service_key, tags)

print("Done!")
