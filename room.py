import logging
import sys

import requests

class Room:
    def __init__(self, alias):
        self.alias = alias
        self.visible_domain = alias.split(":")[1]
        self.alias_urlenc = requests.utils.quote(alias)
        r = requests.get(
            "https://" + self.visible_domain + "/.well-known/matrix/server"
        )
        if r.status_code == 200:
            self.connection_string = r.json()["m.server"]
        else:
            self.connection_string = self.visible_domain + ":443"
        r = requests.get(
            "https://"
            + self.connection_string
            + "/_matrix/client/r0/directory/room/"
            + self.alias_urlenc
        )
        if r.status_code == 200:
            self.id = r.json()["room_id"]
            self.id_urlenc = requests.utils.quote(self.id)
        else:
            raise ValueError("Could not resolve room id")

    def promote_admin(self, user_id_to_promote, server_admin_access_token):
        headers = {
            "Authorization": "Bearer " + server_admin_access_token,
            "Content-Type": "application/json",
        }
        payload = {"user_id": user_id_to_promote}
        r = requests.post(
            "https://"
            + self.connection_string
            + "/_synapse/admin/v1/rooms/"
            + self.alias_urlenc
            + "/make_room_admin",
            json=payload,
            headers=headers,
        )
        if r.status_code == 200:
            print("Promoted " + user_id_to_promote + " admin in room " + self.alias)
            logging.info(
                "Promoted " + user_id_to_promote + " admin in room " + self.alias
            )
        else:
            print(
                "Failed to promote "
                + user_id_to_promote
                + " admin in room "
                + self.alias,
                file=sys.stderr,
            )
            logging.error(
                "Failed to promote "
                + user_id_to_promote
                + " admin in room "
                + self.alias,
                file=sys.stderr,
            )
            print("Reason: " + r.text, file=sys.stderr)
            logging.error("Reason: " + r.text)

    def add_user(self, user_id_to_add, server_admin_access_token):
        headers = {
            "Authorization": "Bearer " + server_admin_access_token,
            "Content-Type": "application/json",
        }
        payload = {"user_id": user_id_to_add}
        r = requests.post(
            "https://"
            + self.connection_string
            + "/_synapse/admin/v1/join/"
            + self.alias_urlenc,
            json=payload,
            headers=headers,
        )
        if r.status_code == 200:
            print("Joined " + user_id_to_add + " to room " + self.alias)
            logging.info("Promoted " + user_id_to_add + " to room " + self.alias)
        else:
            print(
                "Failed to add " + user_id_to_add + " to room " + self.alias,
                file=sys.stderr,
            )
            logging.error(
                "Failed to add " + user_id_to_add + " to room " + self.alias
            )
            print("Reason: " + r.text, file=sys.stderr)
            logging.error("Reason: " + r.text)
