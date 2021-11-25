import argparse
import logging
import sys

import requests

from room import Room

parser = argparse.ArgumentParser(description="Use Synapse admin API to join a user to rooms and promote them admin.")
parser.add_argument("-u", "--user", help="Matrix ID of the user to add to the rooms and promote admin", required=True)
parser.add_argument("-r", "--rooms", help="File containing the list of rooms to which the user should be added", required=True)
parser.add_argument("-t", "--token", help="File containing the Acces Token of the Synapse administrator")
parser.add_argument("-c", "--create", help="Create the room if it doesn't already exist", action="store_true")
args = parser.parse_args()

server_admin_access_token = None

if args.token is not None:
    try:
        file = open(args.token)
        server_admin_access_token = file.read().rstrip()
    except IOError:
        print("Failed to open file "+args.rooms+", does it exist?", file=sys.stderr)
        logging.error("Failed to open file "+args.rooms+", does it exist?")
        sys.exit()
else:
    server_admin_access_token = input("Server Admin Access Token: ")

with open(args.rooms, "r") as f:
    lines = f.readlines()

    for line in lines:
        alias = line.strip()
        try:
            room = Room(alias)
        except ValueError:
            if args.create:
                Room.create(server_admin_access_token, alias)
                room = Room(alias)
            else:
                logging.error("Room "+alias+" doesn't exist.")
                print("Room "+alias+" doesn't exist.", file=sys.stderr)
                break
        if room.visible_domain != args.user.strip().split(":")[1]:
            print("Room "+room.alias+" is on another server than "+args.user.strip()+", skipping", file=sys.stderr)
            logging.error("Room "+room.alias+" is on another server than "+args.user.strip()+", skipping")
            break
        room.add_user(args.user.strip(), server_admin_access_token)
        room.promote_admin(args.user.strip(), server_admin_access_token)
