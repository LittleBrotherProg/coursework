import requests
from progress.bar import ChargingBar
import json


class VK:

   def __init__(self, access_token, user_id, count_photo, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.count_photo = count_photo
       self.params = {'access_token': self.token, 'v': self.version}

   def users_info(self):
       bar_user_info = ChargingBar('Получение данных о фото профиля', max = 100)
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id, 'fields': 'crop_photo'}
       response = requests.get(url, params={**self.params, **params})
       bar_user_info.next(100)
       bar_user_info.finish()
       return response.json()
   
   
   def profile_picture(self):
       bar_profile_picture = ChargingBar('Получение url и колличество лайков на фото', max = 100)
       user_info = vk.users_info()
       id_profile_picture = user_info['response'][0]['crop_photo']['photo']['id']
       bar_profile_picture.next(25)
       album_id = user_info['response'][0]['crop_photo']['photo']['album_id']
       bar_profile_picture.next(25)
       url = 'https://api.vk.com/method/photos.get'
       params= {'owner_id': self.id, 
                'album_id': album_id, 
                'photo_ids': id_profile_picture,
                'extended': '1'
                }
       info_photo = requests.get(url, params={**self.params, **params})
       url_size_photos = {}
       url_size_photos['url_size'] = []
       name_photo = info_photo.json()['response']['items'][0]['likes']['count']
       url_size_photos['file_name'] = name_photo
       info_photo = info_photo.json()['response']['items'][0]['sizes']
       info_photo = sorted(info_photo, key=lambda x: (x['height'] and x['width']), reverse = True)
       for url_type in info_photo:
        if len(url_size_photos['url_size']) == self.count_photo:
            bar_profile_picture.next(25)
            break
        else:
            url_size_photos['url_size'].append({
                'file_url': url_type['url'],
                'size': url_type['type']
            })
        
       bar_profile_picture.next(25)
       bar_profile_picture.finish()
       return url_size_photos
    
class YA():
    def __init__(self, token, url_photo, name_photo, size):
        self.url_photo = url_photo
        self.headers = {
            'Content-Type': 'application/json', 
            'Authorization': token
        }
        self.params = {'path':'disk:/'}
        self.name_folder = 'Фото_профиля_ВК'
        self.name_photo = name_photo
        self.size = size

    def create_folder(self):
        bar_create_folder = ChargingBar('Создание/Проверка папки для фото', max = 100)
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        info_folder = requests.get(url, headers={**self.headers}, params={**self.params})
        count_files = len(info_folder.json()['_embedded']['items'])
        bar_create_folder.next(25)
        for count in range(int(count_files)):
            bar_create_folder.next(25)
            type_files = info_folder.json()['_embedded']['items'][count]['type']
            count_name_folder = info_folder.json()['_embedded']['items'][count]['name']
            if type_files == 'dir':
                if self.name_folder != count_name_folder:
                    params = dict(path = self.params.get('path') + self.name_folder)  
                    requests.put(url, headers={**self.headers}, params={**params})
        bar_create_folder.finish()
        return
        
    def loading_profile_picture(self):
        bar_loading_profile_picture = ChargingBar('Загрузка файла на диск', max = 100)
        load_photo.create_folder()
        bar_loading_profile_picture.next(25)
        url_loading = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        bar_loading_profile_picture.next(25)
        params = dict(path = self.params.get('path') + self.name_folder + '/' + self.name_photo + '.jpg', url = self.url_photo)
        bar_loading_profile_picture.next(25)
        succsesful = requests.post(url_loading, params={**params}, headers={**self.headers})
        bar_loading_profile_picture.next(25)
        info_file = {'file_name':self.name_photo + '.jpg', 'size':self.size }
        bar_loading_profile_picture.finish()
        return succsesful, info_file


with open(r'vk_token.txt') as vk_token:
    vk_token = vk_token.read()
with open (r'YA_token.txt') as YA_token:
    YA_token = YA_token.read()
with open (r'vk_id.txt') as vk_id:
    vk_id = vk_id.read()
#vk = input('Введите свой ID из вк' '\n')
count_photo = input('Введите колличество загружаемых фото')
if count_photo == '':
    count_photo = 5
else:
    count_photo = int(count_photo)
vk = VK(vk_token, vk_id, count_photo)
info_photo = vk.profile_picture()
data_info = []
for showdown in info_photo['url_size']:
    url = showdown['file_url']
    size = showdown['size']
    name = info_photo['file_name']
    load_photo = YA(YA_token, url, str(name), size)
    check  = load_photo.loading_profile_picture()
    if str(check[0]) == '<Response [202]>':
        data_info.append(check[1])
        print('Succsesful')
    else:
        print('Mistake', str(check[0]))
with open(r'info_load_photo.json', 'w') as info:
    json.dump(data_info, info)

