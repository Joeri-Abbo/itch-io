import json
from helper import fetch_games_of_creators, get_creators
data_dir = "data"
fetch_games_of_creators(get_creators(), data_dir)