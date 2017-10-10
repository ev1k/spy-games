from urllib.parse import urljoin
import requests
import json
from time import sleep

TOKEN = ''
VERSION = '5.67'
USER_ID = ''


class VkBase:
    API_URL = 'https://api.vk.com/method/'

    def get_params(self,
                   user_id=None,
                   group_id=None,
                   extended=None,
                   fields=None):
        return {
            'access_token': self.token,
            'v': self.version,
            'user_id': user_id,
            'group_id': group_id,
            'extended': extended,
            'fields': fields
        }


class VkApi(VkBase):
    def __init__(self, token, version):
        self.token = token
        self.version = version

    def get_friends(self, user_id):
        url = urljoin(self.API_URL, 'friends.get')
        params = self.get_params(user_id=user_id)
        try:
            response = requests.get(url, params=params)
            return response.json()['response']['items']
        except requests.exceptions.RequestException as e:
            print('requests.exceptions.RequestException: {}'.format(e))
        finally:
            return []

    def get_groups(self, user_id, extended=None, fields=None):
        url = urljoin(self.API_URL, 'groups.get')
        params = self.get_params(
            user_id=user_id,
            extended=extended,
            fields=fields
        )
        try:
            response = requests.get(url, params=params)
            return response.json()['response']['items']
        except requests.exceptions.RequestException as e:
            print('requests.exceptions.RequestException: {}'.format(e))
        finally:
            return []

    def get_group_info(self, group_id, fields):
        url = urljoin(self.API_URL, 'groups.getById')
        params = self.get_params(group_id=group_id, fields=fields)
        try:
            response = requests.get(url, parms=params)
            return response.json()['response']
        except requests.exceptions.RequestException as e:
            print('requests.exceptions.RequestException: {}'.format(e))
        finally:
            return []


def write_json(data):
    with open('groups.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)


if __name__ == '__main__':
    vk = VkApi(TOKEN, VERSION)
    friends_vk = vk.get_friends(USER_ID)
    count_friends = len(friends_vk)
    groups_vk = vk.get_groups(USER_ID)
    set_my_groups = set(groups_vk)
    for friend in friends_vk:
        friend_groups = vk.get_groups(friend)
        set_friend_group = set(friend_groups)
        if set_my_groups & set_friend_group:
            set_my_groups -= (set_my_groups & set_friend_group)
        count_friends -= 1
        print('.')
        print('Осталось обработать {} друзей'.format(count_friends))
        sleep(0.34)
    data_list = []
    for group in set_my_groups:
        group_info = vk.get_group_info(group, 'members_count')
        sleep(0.34)
        dict_to_json = {
            'id': group_info[0]['id'],
            'name': group_info[0]['name'],
            'members_count': group_info[0]['members_count']
        }
        data_list.append(dict_to_json)
    write_json(data_list)



