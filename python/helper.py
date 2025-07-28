import os
import json
import requests
from bs4 import BeautifulSoup
import os

def get_all_directories(path):
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

def get_creators()-> list:
    with open('creators.json', 'r') as f:
        creators = json.load(f)
    return creators

def add_creator(creator: str):
    creators = get_creators()
    if creator not in creators:
        creators.append(creator)
        with open('creators.json', 'w') as f:
            json.dump(creators, f, indent=4)
        print(f"Added {creator} to creators.json")
    else:
        print(f"{creator} already exists in creators.json")



def get_data_dir():
    return "../frontend/public/data"


def fetch_games_of_creators(
    creators: list
):
    for creator in creators:
        fetch_games_of_creator(creator)

def fetch_games_of_creator(
    creator: str
):
    data_dir = get_data_dir()
    url = f"https://{creator}.itch.io/"
    # fetch html of page
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        # parse html to get game info
        soup = BeautifulSoup(html, 'html.parser')
        # write to index.html in current directory
        
        

        games = soup.find_all('a', class_='game_link')
        print(f"Found {len(games)} games for creator {creator}")

        for game in games:
            game_link = game['href']
            
            # get game name after itch.io/
            game_name = game_link.split('/')[-1]
            print(f"Game name: {game_name}")
            
            # create directory for creator if it does not exist
            creator_dir = f"{data_dir}/{creator}"
            if not os.path.exists(creator_dir):
                os.makedirs(creator_dir)
            # check if game file already exists
            game_file_path = f"{creator_dir}/{game_name}.json"
            if os.path.exists(game_file_path):
                print(f"Game file {game_file_path} already exists, skipping.")
                continue
            data = requests.get(f"{game_link}/data.json").json()
            if data:
                with open(game_file_path, 'w') as game_file:
                    json.dump(data, game_file, indent=4)
                    print(f"Created {game_name}.json for {creator} in {creator_dir}/")
    else:
        print(f"Failed to fetch page for {creator}, status code: {response.status_code}")