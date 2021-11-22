import logging
import requests
import sys
from room import Room

user_id_to_promote = sys.argv[1]

server_admin_access_token = input("Server Admin Access Token: ")

with open(sys.argv[2],'r') as f:
	lines = f.readlines()

	for line in lines:
		room = Room(line.strip())
		room.add_user(user_id_to_promote, server_admin_access_token)
		room.promote_admin(user_id_to_promote, server_admin_access_token)
