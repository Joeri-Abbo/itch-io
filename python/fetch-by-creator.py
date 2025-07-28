import argparse
import json

from helper import fetch_games_of_creator, add_creator

parser = argparse.ArgumentParser(description="Example script")
parser.add_argument("creator", help="The creator's username")
args = parser.parse_args()
creator = args.creator
print(f"Fetching games for creator: {creator}")
add_creator(creator)

fetch_games_of_creator(creator)
print(f"Games for creator {creator} fetched successfully.")