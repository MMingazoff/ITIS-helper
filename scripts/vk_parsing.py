import requests
import re
from typing import List, Tuple
from config import ACCESS_TOKEN


MAX_POSTS = 10


def from_id_to_url(post_txt: str) -> str:
    """Текст типа [id01|Павел] преобразуется в ссылку"""
    found_data = re.findall(r'\[[^]]+\]', post_txt)
    new_post_txt = post_txt
    if found_data:
        for link in found_data:
            user, name = link[1:-1].split('|')
            if user.startswith('id'):
                new_url = f'<a href="https://vk.com/{user}">{name}</a>'
            else:
                new_url = f'<a href="{user}">{name}</a>'
            new_post_txt = re.sub(r'\[[^]]+\]', new_url, new_post_txt, count=1)
    return new_post_txt


def get_posts(group_name: str, max_posts: int = MAX_POSTS, pinned_posts: int = 0) -> List[Tuple[str, str]]:
    """На вход подется навание группы. Возвращается список из последних 10 постов и ссылок на них"""
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count={max_posts}&offset={pinned_posts}" \
          f"&access_token={access_token}&v=5.131"
    request = requests.get(url)
    source = request.json()
    posts = source["response"]["items"]
    result = []
    for post in posts:
        result.append((from_id_to_url(post["text"]),
                       f"https://vk.com/{group_name}?w=wall{post['from_id']}_{post['id']}"))
    return result


def get_request_posts(max_post: int = MAX_POSTS) -> List[Tuple[str, str]]:
    """Возвращается список из последних 10 постов в группе реквеста и ссылок на них"""
    return get_posts("itis_request", max_posts=max_post + 1, pinned_posts=1)


def get_du_posts(max_post: int = MAX_POSTS) -> List[Tuple[str, str]]:
    """Возвращается список из последних 10 постов в группе 18 дома и ссылок на них"""
    posts = get_posts("universiade_village18", 20)
    # дальше идет удаление постов без текста (посты о смене постельного белья)
    posts_to_delete = []
    for post_num in range(len(posts)):
        if not posts[post_num][0]:  # проверка на пустой текст поста
            posts_to_delete.append(post_num)
    posts = [posts[i] for i in range(len(posts)) if i not in posts_to_delete]
    return posts[:max_post]
