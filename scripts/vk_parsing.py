import requests
import re
from typing import List, Tuple
from vk_auth import access_token


MAX_POSTS = 10


def from_id_to_url(post_txt: str) -> str:
    """Текст типа [id01|Павел] преобразуется в ссылку"""
    found_data = re.findall(r'\[.+\]', post_txt)
    new_post_txt = post_txt
    if found_data:
        user_id, name = found_data[0][1:-1].split('|')
        # new_url = f'[{name}](https://vk.com/{user_id})'
        new_url = f'<a href="https://vk.com/{user_id}">{name}</a>'
        new_post_txt = re.sub(r'\[.+\]', new_url, new_post_txt)
    return new_post_txt


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
        result.append((from_id_to_url(post["text"]),
                       f"https://vk.com/itis_request?w=wall{post['from_id']}_{post['id']}"))
    return result
