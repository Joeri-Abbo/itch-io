from bs4 import BeautifulSoup
import requests
import json


def fetch_tags(url:str)->list:
    items = []
    response = requests.get(url)
    print(f"Fetching tags from {url}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # find all elements with class "tag_title"
        tags = soup.find_all(class_="tag_title")
        print("Fetched tags:")
        for tag in tags:
            print(tag)
            print("BEFORE APPEND")
            items.append(
                {
                    "name": tag.text.strip(),
                    "url": tag['href']
                }
            )
            print("AFTER APPEND")

    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
    return items
        
    

if __name__ == "__main__":
    url = "https://itch.io/tags?page="
    #open tags.json and read it
    with open('tags.json', 'r') as f:
        tags = json.load(f)
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    pager = soup.find(class_="pager")
    if pager:
        pager_label = pager.find(class_="pager_label")
        if pager_label:
            # fetch a tag and get href
            last = pager_label.find('a')
            if last:
                max_page = last['href'].split('=')[-1]
    counter = 1
    while counter <= int(max_page):
        response = requests.get(f"{url}{counter}")
        for tag in fetch_tags(f"{url}{counter}"):
            if tag not in tags:
                tags.append(tag)
        counter += 1
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
    # write tags to tags.json
    with open('tags.json', 'w') as f:
        json.dump(tags, f, indent=4)
    print(f"Saved {len(tags)} tags to tags.json")
        
        
    