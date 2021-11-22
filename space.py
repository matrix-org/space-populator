import logging
import requests
import sys


class Space:
    def __init__(self, space_id, access_token):
        self.id = space_id
        self.id_urlenc = requests.utils.quote(space_id)
        self.visible_domain = space_id.split(":")[1]
        r = requests.get(
            "https://" + self.visible_domain + "/.well-known/matrix/server"
        )
        if r.status_code == 200:
            self.connection_string = r.json()["m.server"]
        else:
            self.connection_string = self.visible_domain + ":443"
        self.access_token = access_token

    def add_room(self, room):
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json",
        }
        payload = {"via": [room.visible_domain]}
        r = requests.put(
            "https://"
            + self.connection_string
            + "/_matrix/client/r0/rooms/"
            + self.id_urlenc
            + "/state/m.space.child/"
            + room.id_urlenc,
            json=payload,
            headers=headers,
        )
        if r.status_code == 200:
            print("Added " + room.alias + " to space " + self.id)
            logging.info("Added " + room.alias + " to space " + self.id)
        else:
            print(
                "Failed to add " + room.alias + " to space " + self.id, file=sys.stderr
            )
            logging.error("Failed to add " + room.alias + " to space " + self.id)
            print("HTTP Status: " + r.status_code, file=sys.stderr)
            logging.error("HTTP Status: " + r.status_code)
            print("Reason: " + r.text, file=sys.stderr)
            logging.error("Reason: " + r.text)
