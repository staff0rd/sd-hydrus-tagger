import argparse

from loguru import logger
from tqdm import tqdm

from src.api import HydrusApi
from src.utils import get_comfyui_tags

parser = argparse.ArgumentParser(
    description="Apply stable diffusion tags to images in Hydrus"
)
parser.add_argument("command")
parser.add_argument("-h", "--host", default="http://localhost:45869")
parser.add_argument("-k", "--access-key", required=True)
args = parser.parse_args()
host = args.host
access_key = args.access_key

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
