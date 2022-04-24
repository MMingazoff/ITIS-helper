import requests
from typing import List, Tuple
from vk_auth import access_token


MAX_POSTS = 10


def get_posts(group_name: str) -> List[Tuple[str, str]]:
    """На вход подется навание группы. Возвращается список из последних 10 постов и ссылок на них"""
    pinned_post = 1 if group_name == "itis_request" else 0
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count={MAX_POSTS}&offset={pinned_post}" \
          f"&access_token={access_token}&v=5.131"
    request = requests.get(url)
    source = request.json()
    posts = source["response"]["items"]
    result = []
    for post in posts:
        result.append((post["text"],
                       f"https://vk.com/itis_request?w=wall{post['from_id']}_{post['id']}"))
    return result
