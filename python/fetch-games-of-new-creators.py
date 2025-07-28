from helper import get_creators, get_data_dir,get_all_directories, fetch_games_of_creator

# get all folders in data directory
data_dir = get_data_dir()
creators = get_all_directories(data_dir)

no_new_creators = True
for creator in get_creators():
    if creator not in creators:
        print(f"New creator found: {creator}")
        try:
            fetch_games_of_creator(creator)
        except Exception as e:
            print(f"Error fetching games for creator {creator}: {e}")
        no_new_creators = False

if no_new_creators:
    print("No new creators found.")