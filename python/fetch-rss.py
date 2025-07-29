import requests
import xml.etree.ElementTree as ET
import json
from helper import get_creators, add_creator
import argparse
# https://itch.io/games/free.xml
# https://itch.io/game-assets/tag-effects.xml
# http://itch.io/feed/new.xml


parser = argparse.ArgumentParser(description="Example script")
parser.add_argument("feed", help="The RSS feed URL to fetch")
args = parser.parse_args()
feed = args.feed


def fetch_xml(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None


def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = {}
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                if k in dd:
                    if not isinstance(dd[k], list):
                        dd[k] = [dd[k]]
                    dd[k].append(v)
                else:
                    dd[k] = v
        d = {t.tag: dd}
    if t.text and t.text.strip():
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['text'] = text
        else:
            d[t.tag] = text
    return d


import os

if __name__ == "__main__":
    data_dir = "rss_data"
    # Create the data directory if it does not exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # load in creators.json
    creators = get_creators()

    print("fetch.py module loaded successfully.")
    xml_data = fetch_xml(feed)
    if xml_data:
        print("XML data fetched successfully.")
        try:
            root = ET.fromstring(xml_data)
            xml_dict = etree_to_dict(root)
            items = xml_dict.get('rss').get('channel')
            for item in items.get('item', []):

                link = item['link']
                username = link.split('/')[2].split('.')[0]
                game = link.split('/')[3] if len(link.split('/')) > 3 else None
                creators.append(username)
                add_creator(username)

                if not os.path.exists(f"{data_dir}/{username}"):
                    os.makedirs(f"{data_dir}/{username}")
                with open(f"{data_dir}/{username}/{game}.json", 'w') as game_file:
                    json.dump(item, game_file, indent=4)
                    print(f"Created {game}.json for {username} in {data_dir}/{username}/")

        except ET.ParseError as e:
            print(f"Error parsing XML data: {e}")
    else:
        print("Failed to fetch XML data.")
