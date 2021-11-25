# Space Populator

## Who is this for?

This repository should contain useful tools for you if:
* You are already familiar with Matrix Spaces and want to build your own for your community
* Your community relies on IRC, on Libera Chat, OFTC, or one of the other networks already bridged to Matrix (e.g. GIMPnet) and you want to boost your presence on Matrix

## What should I know?

### What's a Space?

A Matrix Space can be many things, but from the perspective of an open community, it is a convenient way to group all the rooms together so people can explore and join them. You can think about it as a directory.

![](./docs/img/space_preview.png)

### Do I need those scripts?

You don't strictly need those scripts for anything! They are just helper to put things together faster, but you can do everything by hand if you want to take the time to do it.

### We're already on Matrix, how do I create a Space?

⚠️ **IMPORTANT NOTE:** The `permator` script makes use of the Synapse admin API. It will send the server admin access token to synapse, so you need to make sure all the rooms you want to perform an action against have a `:yourserver.tld` domain. The script will warn you and exit if you try to send your token to other servers.

The steps to create a space are simple here:
1. Narrow down which space should welcome the new room
1. List all the rooms that should land in that space
1. Run the permator script to join a user to these rooms and grant them privileges (useful e.g. for the moderation bot). The permator script can also create the rooms if they don't already exist.
1. Run the populator script to add the rooms to the Space

You need to have `git`, `python` and `pipenv` installed on your machine.

1. Clone this project. Assuming you have git installed on your machine, `git clone https://github.com/matrix-org/space-populator.git`
1. Gather a list of all your rooms and put them in a file called `my_rooms.txt`, with one room alias per line.
1. `cd` to the project directory, and run `pipenv install` and then `pipenv shell` so python has all the dependencies needed to execute the script
1. In Element, click on your profile picture, and in the menu click on All Settings. Go to the "Help & About" tab, scroll to the bottom, and expand the "Access Token" item. You can copy your Access Token.. Save that access token in a file called `access_token.txt` next to the python script.
1. In the terminal, run `python permator.py -u <MatrixID of the user to promote admin> -r my_rooms.txt -t access_token.txt -d mydomain.tld`. You can optionally add ` -c` at the end so the script creates the room if they don't already exist.
1. Create the space in Element
1. Retrieve the Space ID. To do so, click on the hash and magnifier sign next to the search bar in the left panel of your Space. Then click on the gear next to invite. Go to the "Advanced" tab: the internal room ID under "Space information" is your Space id. You can close the modal.
1. In the terminal where you ran the `pipenv` commands, run `python populator.py -s "<the space id of the space to which you want to add rooms>" -r ./my_rooms.txt -t access_token.txt`. Take care of escaping the `!` of the space id by adding a `\` before it!
1. The script is going to ask you your Access Token. Go to Element, click on your profile picture, and in the menu click on All Settings. Go to the "Help & About" tab, scroll to the bottom, and expand the "Access Token" item. You can copy your Access Token.
1. The script will generate a file called `populator.log` to tell you which room was successfully added and which one was not.
1. Don't forget to remove the `access_token.txt` file!

### We're on IRC, how do we create a Space

Two cases can exist:
1. You community already exists on Libera Chat, OFTC, or another network which is bridged to Matrix: good news! You're already on Matrix and can follow the  steps above.
  1. If you are on Libera Chat, the rooms aliases of your channel are `#<your_channel_name>:libera.chat`
  1. If you are on OFTC, the room aliases of your channel are `#_oftc_#<your_channel_name>:matrix.org`
1. Your communit is not yet on Matrix: I'm working on an article explaining how to carry out the change in your community, with links to how you can (and most probably should) set-up a bridge.

### We're new on Matrix, how do we create a Space

Element's UI will allow you to create a Space fairly easy, but this can be quite combersome if you want to create a large number of rooms.

This script will later add a feature to create new rooms and add them to your Space.