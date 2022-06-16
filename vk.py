import time
import requests
from pprint import pprint
from typing import Callable, Iterator, Union, Optional


class Vk:
    URL = 'https://api.vk.com/method/'
    
    def __init__(self, token):
        '''
        Метод инициализации экземпляра класса по токену вк.
        '''
        self.params = {
            'access_token': token,
            'v': '5.131'
        }
        self.user_id = ''
        self.user_albums = {}
        self.user_album_id = ''
        self.user_photos = []

    def get_user_id(self, inp_name: str) -> bool:
        '''
        Метод определения имени и фамилии владельца фотографий, доступных для копирования.
        '''
        user_info_url = self.URL + 'users.get'
        user_info_params = {
            'user_ids': inp_name.strip(),
            'deactivated': None,
            'can_access_closed': None
        }
        resp = 0
        resp = requests.get(user_info_url, params={**self.params, **user_info_params})
        id_status = False
        if resp.json()['response'] == []:
            print('Страница не существует')
            id_status = False
        elif 'deactivated' in resp.json()["response"][0].keys():
            print('Страница удалена или забанена')
            id_status = False
        elif resp.json()["response"][0]["can_access_closed"] is False:
            print('Закрытый профиль')
            id_status = False
        elif resp.json()['response'][0]["can_access_closed"]:
            print(f'Пользователь {resp.json()["response"][0]["first_name"]} \
{resp.json()["response"][0]["last_name"]}')
            self.user_id = resp.json()["response"][0]["id"]
            id_status = True
        return id_status

    def get_albums(self):
        '''
        Метод получения доступных альбомов пользователя.
        '''
        albums_url = self.URL + 'photos.getAlbums'
        albums_params = {
            'owner_id': self.user_id,
            'need_system': 1,
            'tags': None
        }
        response = requests.get(albums_url, params={**self.params, **albums_params})
        albums = {}
        counter = 0
        for element in response.json()['response']['items']:
            if response.json()['response']['count'] == 0:
                continue
            counter += 1
            albums[counter] = element['id'], element['title'], element['size']
            pprint(f'{counter}: {element["title"]}, {element["size"]} фото')
        self.user_albums = albums

    def select_album(self, inp_number: str) -> str:
        '''
        Метод выбора альбома для копирования.
        '''
        if inp_number.strip() == '':
            self.user_album_id = '-6'
            print('Номер альбома не введён. Копирование из аватарок.')
        elif inp_number.strip() in str(self.user_albums.keys()) and self.user_albums[int(inp_number)][-1] != 0:
            self.user_album_id = str(self.user_albums[int(inp_number)][0])
            print(f'Выбран альбом {self.user_albums[int(inp_number)][1]}')
        elif inp_number.strip() in str(self.user_albums.keys()) and self.user_albums[int(inp_number)][-1] == 0:
            self.user_album_id = '-6'
            print('В выбранном альбоме нет фотографий. Копирование из аватарок.')  
        else:
            self.user_album_id = '-6'
            print('Номер альбома не определён. Копирование из аватарок.')        
        return self.user_album_id

    def __get_json(self):
        '''
        Метод получения json файла с фотографиями.
        -9000 - id альбома фотографий, на которых отмечен пользователь.
        '''
        photos_params = {
            'extended': 1,
            'photo_sizes': 1,
            'count': 1000
        }
        if self.user_album_id == '-9000':
            photos_url = self.URL + 'photos.getUserPhotos'
            id_params = {
            'user_id': self.user_id            
        }
        else:
            photos_url = self.URL + 'photos.get'
            id_params = {
            'owner_id': self.user_id,
            'album_id': self.user_album_id
        }
        response = requests.get(photos_url, params={**self.params, **id_params, **photos_params}).json()
        return response

    def get_photos(self, inp_photo_q: str) -> list:
        '''
        Метод получения фотографий для копирования.
        '''
        resp = self.__get_json()
        photos = {}
        for item in resp['response']['items']:
            # для имени фото используем количество лайков
            name_of_photo = str(item['likes']['count'])
            date_of_photo = str(time.strftime("%d_%m_%y_%H_%M_%S", time.localtime(item['date'])))
            # переименовываем фото, когда количество лайков одинаково
            for element in photos:
                if name_of_photo in photos.keys():
                    name_of_photo +='_' + date_of_photo
            # из одноимённых фото выбираем только фото максимального размера
            photo = {}
            photo_resol = 0
            photo_resol_max = 0
            for element in item['sizes']:
                photo_resol = int(element['height']) * int(element['width'])
                if photo_resol_max <= photo_resol:
                    photo_resol_max = photo_resol
                    photo_url = element['url']
                    photo_type = element['type']
            # наполняем словарь фотографий
            photo = (photo_resol, photo_url, photo_type)
            photos.setdefault(name_of_photo, photo)
        # преобразуем словарь в список для сортировки по величине фото
        photos_list = list(photos.items())
        sorted_photo = sorted(photos_list, key=lambda x: x[1], reverse=True)
        # берём указанное количество фото
        if inp_photo_q.strip().isnumeric():
            inp_photo_q = int(inp_photo_q)
        else:
            inp_photo_q = 5

        for photo in sorted_photo[:int(inp_photo_q)]:
            photo_dict = {'url': photo[1][1], 'file_name': photo[0], 'size': photo[1][2]}
            self.user_photos.append(photo_dict)
        return self.user_photos