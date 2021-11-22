import logging
import sys

from room import Room
from space import Space

logging.basicConfig(filename="populator.log", filemode="w", level=logging.INFO)

with open(sys.argv[2], "r") as f:
    lines = f.readlines()

    access_token = input("Access Token: ")
    space = Space(sys.argv[1], access_token)

    for line in lines:
        room = Room(line.strip())
        space.add_room(room)
