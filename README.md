# sd-hydrus-tagger
Tag hydrus images with embedded Stable Diffusion metadata

## Install

```shell
git clone https://github.com/staff0rd/sd-hydrus-tagger
cd sd-hydrus-tagger
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Hydrus setup

1. Apply the tag `sd:pending` to anything you want processed
    1. Add this tag when importing from stable diffusion output folders
1. Enable the Client API:
    1. services > manage services > client api > run the client api > enable
    1. services > review services > client api > add > from api request

## Running

```shell
python main.py request-permissions # only needed once, accept the permissions in hydrus and copy the access key
python main.py process -k <access key from above> process-images
```

## Help

```shell
python main.py --help
python main.py process-images --help
```