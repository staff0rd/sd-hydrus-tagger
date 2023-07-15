import argparse


def get_command():
    parser = argparse.ArgumentParser(
        prog="main.py", description="Apply stable diffusion tags to images in Hydrus"
    )
    parser.add_argument(
        "--host", default="http://localhost:45869", help="hydrus client api host"
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser(
        "request-permissions", help="returns an access key to pass to other commands"
    )

    parser_process_images = subparsers.add_parser(
        "process-images", help="process images"
    )
    parser_process_images.add_argument(
        "-k",
        "--access-key",
        required=True,
        help="hydrus client api access key - call request-permissions to get this",
    )
    parser_process_images.add_argument(
        "-f",
        "--force",
        help="force reprocessing of images that have already been processed",
        action=argparse.BooleanOptionalAction,
    )
    parser_process_images.add_argument(
        "-t",
        "--extra-tags",
        nargs="+",
        help="only process images with these tags",
    )

    return (parser.parse_args(), parser)
