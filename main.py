from tqdm import tqdm

from src.api import HydrusApi
from src.commands import get_command
from src.utils import get_comfyui_tags

args, parser = get_command()
host = args.host
command = args.command

if command == "request-permissions":
    api = HydrusApi(host, "", "")
    result = api.request_permissions([2, 3])
    print(result)

elif command == "process-images":
    api = HydrusApi(host, args.access_key)
    file_ids = api.get_files_to_process(args.extra_tags, force=args.force)
    service_key = api.get_tag_service_key()
    if service_key is None:
        raise Exception("No tag service found")

    image_count = len(file_ids)
    print(f"Found {image_count} images to process")

    if image_count > 0:
        print("Processing images...")

        for file_id in tqdm(file_ids):
            image = api.get_image(file_id)
            tags = get_comfyui_tags(image)
            api.add_tags(file_id, service_key, tags)

    print("Done!")

else:
    print(f"Unknown command: {command}")
    parser.print_help()
    exit(1)
