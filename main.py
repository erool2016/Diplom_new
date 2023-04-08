from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import Data_Base

from operator import itemgetter
import config_bot
from start_bot import start



vk = vk_api.VkApi(token=config_bot.token_vkinder_servis_key)
vk2 = vk_api.VkApi(token=config_bot.tok111)
longpoll = VkLongPoll(vk)



def write_msg(user_id, message,attachment=None):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),'attachment':attachment})

def session_longpoll():
    '''получаем ответ в чате бота'''

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            user_id = event.user_id
            write_msg(user_id, f"Хай, {event.user_id}")
            request_user  = event.text.lower()



            return request_user,user_id




def get_user_foto(i):
    '''Принимает список айди  возвращает список списков [ количество лайков,самых популярных id] '''
    list = []

    session = vk_api.VkApi(token=config_bot.tok111)
    response = session.method('photos.get', {
        'owner_id': i,
        'album_id': 'profile',
        'extended': 1,
        'photo_sizes': 1})
    a = response['items']

    for item in a:

        list.append(item['likes']['count'])
        url = item['sizes'][0]['url']

    return list,url

def presentation(list,user_id):

    n=0
    while n < 3:

        write_msg(user_id,f'{list[n][1]},{list[n][2]},"лайков",{list[n][3]}',attachment=list[n][4])
        n+=1



def what_to_do(user_id,list):
    print(user_id,list)
    write_msg(user_id,'Что будем делать далее ( w - смотреть далее / другая кнопка - новый поиск)',attachment=None)
    answer, user_id = session_longpoll()
    if answer == 'w':
        print(answer)
        create_list_for_prezentation(list,user_id)
    if answer != 'w':
        print(answer)
        start()


def save_db(lists,user_id,list_for_view):
    print('list for save',lists)
    for list in lists:
        Data_Base.save_tabel_data_user(list)
    what_to_do(user_id,list_for_view)


def create_list_for_prezentation(list,user_id):

    list_for_prezenatation = []
    for i in list:
        a = Data_Base.send_db(i[0])
        if a == None:
            list_for_prezenatation.append(i)
            if len(list_for_prezenatation) == 3:
                presentation(list_for_prezenatation,user_id)

                del list[0]
                save_db(list_for_prezenatation,user_id,list)
        else:
            print('есть в базе', i)

def sorted_list(list,user_id):


    list = (sorted(list, key=itemgetter(3), reverse=True))
    print('отсортированный список',list)
    create_list_for_prezentation(list,user_id)


def get_foto_likes_list(list,user_id):
    '''получаем список с ай ди, имя,фамилия и получаем лайки с фото'''

    for items in list:
        lists, url = get_user_foto(items[0])
        items.append(sum(lists))
        items.append(url)

    sorted_list(list,user_id)




def creating_a_list(resp,user_id):

    result = []

    for i in resp:
        r = []
        if i['is_closed'] == False:
            r.append(i['id'])
            r.append(i['first_name'])
            r.append(i['last_name'])

            result.append(r)

    get_foto_likes_list(result,user_id)

def find_users(data_user_for_find,user_id):
    n = data_user_for_find['bdate'].split('.')

    resp = vk2.method('users.search', {
        #'age_from' : int(n[2]) - 3, вот здесь я так и не понял почему - но если раскоментировать строку - все падает
        'age_to' : int(n[2]) + 3,
        'sex': data_user_for_find['sex'],
        'city': data_user_for_find['city'],
        'fields': 'bdate,sex,photo_id,about,city,relation,inerests,domain',
        'status': 6,
        'count': 25,
        'has_photo': 1,
        'v': 5.131
    })

    creating_a_list(resp['items'],user_id)



