import argparse
import logging
import sys

from room import Room
from space import Space

logging.basicConfig(filename="populator.log", filemode="w", level=logging.INFO)

parser = argparse.ArgumentParser(description="Populate a Matrix Space with a list of rooms.")
parser.add_argument("-s", "--space", help="ID of the space to which the rooms should be added", required=True)
parser.add_argument("-r", "--rooms", help="File containing the list of rooms to add to the Space", required=True)
parser.add_argument("-t", "--token", help="File containing the Acces Token of the person performing the actions")
args = parser.parse_args()

with open(args.rooms, "r") as f:
    lines = f.readlines()

    if args.token is not None:
        try:
            file = open(args.rooms)
            data = file.read().rstrip()
        except IOError:
            print("Failed to open file "+args.rooms+", does it exist?", file=sys.stderr)
            logging.error("Failed to open file "+args.rooms+", does it exist?", file=sys.stderr)
            sys.exit()
    else:
        access_token = input("Access Token: ")
    
    space = Space(args.space.strip(), access_token)
    
    for line in lines:
        room = Room(line.strip())
        space.add_room(room)
