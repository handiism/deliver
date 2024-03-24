import argparse
import json
import os


json_path = os.path.expanduser("~") + "/.swarm-service.json"


def init_action(_):
    exists = os.path.exists(json_path)
    if exists:
        print(f"JSON database already exists at {json_path}")
        exit(1)
    else:
        f = open(json_path, "w")
        f.write("{}")
        f.close()
        print(f"Successfully created JSON DATABASE at {json_path}")


def add_action(args):
    r = open(json_path, "r")
    data = json.load(r)
    r.close()

    safe_image_tag = None
    if args.safe_image_tag != None:
        safe_image_tag = args.safe_image_tag

    if args.service in data:
        data[args.service]["safeImageTag"] = safe_image_tag
    else:
        data[args.service] = {"safeImageTag": safe_image_tag}

    json_data = json.dumps(data, indent=2)

    w = open(json_path, "w")
    w.write(json_data)
    w.close()


def set_action(args):
    r = open(json_path, "r")
    data = json.load(r)
    r.close()

    safe_image_tag = None
    if args.safe_image_tag != None:
        safe_image_tag = args.safe_image_tag

    if args.service in data:

        data[args.service]["safeImageTag"] = safe_image_tag
    else:
        print("There is no service entry with name {args.service}")
        exit(1)

    json_data = json.dumps(data, indent=2)

    w = open(json_path, "w")
    w.write(json_data)
    w.close()


def rm_action(args):
    r = open(json_path, "r")
    data = json.load(r)
    r.close()

    if args.service in data:
        data.pop(args.service)

    json_data = json.dumps(data, indent=2)

    w = open(json_path, "w")
    w.write(json_data)
    w.close()


def print_action(args):
    r = open(json_path, "r")
    print(r.read())
    r.close()


def main():
    parser = argparse.ArgumentParser(
        description="Deliver: CLI tool to manage latest safe docker swarm services"
    )
    subparsers = parser.add_subparsers(title="action", dest="action")

    # Subparser for 'init' command
    init_parser = subparsers.add_parser("init", help="create empty service entry")
    init_parser.set_defaults(func=init_action)

    # Subparser for 'add' command
    add_parser = subparsers.add_parser("add", help="add entry to database")
    add_parser.add_argument("service", help="service to add")
    add_parser.add_argument(
        "--safeImageTag",
        dest="safe_image_tag",
        help="last image with tag that succesfully deploy the service",
    )
    add_parser.set_defaults(func=add_action)

    # Subparser for 'set' command
    set_parser = subparsers.add_parser("set", help="set service configuration")
    set_parser.add_argument("service", help="service to set")
    set_parser.add_argument(
        "safe_image_tag",
        help="last image with tag that succesfully deploy the service",
    )
    set_parser.set_defaults(func=set_action)

    # Subparser for 'rm' command
    rm_parser = subparsers.add_parser("rm", help="remove service entry")
    rm_parser.add_argument("service", help="service to remove")
    rm_parser.set_defaults(func=rm_action)

    # Subparser for 'print' command
    print_parser = subparsers.add_parser("print", help="print database entries")
    print_parser.set_defaults(func=print_action)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
