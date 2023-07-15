import json


def find_json_value(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                yield from find_json_value(v, lookup_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from find_json_value(item, lookup_key)


def get_comfyui_tags(image):
    tags = []
    items = image.info or {}
    if "prompt" in items:
        comfyui_prompt = json.loads(items["prompt"])

        keys = [
            ("ckpt_name", "checkpoint"),
            ("vae_name", "vae"),
            ("lora_name", "lora"),
            ("sample_namer", "sampler"),
            ("text", "prompt"),
        ]

        for key in keys:
            for value in find_json_value(comfyui_prompt, key[0]):
                if len(key) > 1:
                    name = key[1]
                else:
                    name = key[0]

                tags.append(f"sd:{name}:{value}")

        tags = set(tags)
    return tags
