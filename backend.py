import firebase_admin
from firebase_admin.credentials import Certificate
from firebase_admin.firestore import client
from firebase_admin.firestore_async import client as client_async

import settings
import devutils
import requests
import build

credentials = Certificate('json/firebase.json')
app = firebase_admin.initialize_app(credentials, name='GDLiveBackend')
database = client(app)
database_async = client_async(app)

class AccountsPage:
    def __init__(self): ...
    
    def invite_to_collab(self, collab: str, attrabutes: dict, user: str):
        invite_list = {'collab': collab, 'user': settings.user_settings.username, 'attrs': attrabutes}
        profile_dict: dict[list[dict[str]]] = database.collection('Users').document(user).get().to_dict()
        profile_dict['requested_collabs'].append(invite_list)
        database.collection('Users').document(user).update(profile_dict)
    
    def join_collab(self, collab: str):
        usrlist = [None, settings.user_settings.username]
        joined = database.collection('Collabs').document(collab).get().to_dict()['joined_players']
        database.collection('Collabs').document(collab).update({'joined_players', joined.append(usrlist)})

class Editor:
    def __init__(self): ...
    
    def place_object(self, object_id: int, x: int, y: int, rotation: int, editor_layer: int, addrinfo: dict, level: str):
        __base_obj = f'1,{str(object_id)},2,{str(x)},3,{str(y)},4,{str(rotation)},20,{str(editor_layer)},'
        __addr_obj = ''
        for i in addrinfo: devutils.strcat(__addr_obj, f'{i},{__addr_obj[i]}')
        object_string = f'{__base_obj}{__addr_obj},'
        collab_json = database.collection('Collabs').document(level).get().to_dict()
        collab_json['level-file'].append([len(collab_json['level-file']), object_string])
        database.collection('Collabs').document(level).update(collab_json)
    
    def check_object_count(self, level: str) -> int:
        object_list = database.collection('Collabs').document(level).get().to_dict()['level-file']
        return len(object_list)
    
    def move_object(self, x: int, y: int, level: str, object_id: int):
        object_list = database.collection('Collabs').document(level).get().to_dict()
        for i in object_list:
            if i['level-file'][0] == object_id:
                ojs = object_list['level-file'][i][1].split(',')
                ojs[4] = str(x)
                ojs[6] = str(y)
                object_list['level-file'][i][1] = ','.join(ojs)
        database.collection('Collabs').document(level).update(object_list)
    
    def rotate_object(self, angle: int, level: str, object_id: int):
        object_list = database.collection('Collabs').document(level).get().to_dict()
        for i in object_list:
            if i['level-file'][0] == object_id:
                ojs = object_list['level-file'][i][1].split(',')
                ojs[8] = str(angle)
                object_list['level-file'][i][1] = ','.join(ojs)
        database.collection('Collabs').document(level).update(object_list)
    
    def replace_object(self, id: int, level: str, object_id: int):
        object_list = database.collection('Collabs').document(level).get().to_dict()
        for i in object_list:
            if i['level-file'][0] == object_id:
                ojs = object_list['level-file'][i][1].split(',')
                ojs[2] = str(id)
                object_list['level-file'][i][1] = ','.join(ojs)
        database.collection('Collabs').document(level).update(object_list)
    
    def reset_object(self, level: str, object_id: int):
        object_list = database.collection('Collabs').document(level).get().to_dict()
        for i in object_list:
            if i['level-file'][0] == object_id:
                ojs = object_list['level-file'][i][1].split(',')
                object_list['level-file'][i][1] = f'1,{ojs[2]}2,{ojs[4]},3,{ojs[6]},'
        database.collection('Collabs').document(level).update(object_list)
    
    def editor_layer(self, layer: int, level: str, object_id: int):
        object_list = database.collection('Collabs').document(level).get().to_dict()
        for i in object_list:
            if i['level-file'][0] == object_id:
                ojs = object_list['level-file'][i][1].split(',')
                ojs[40] = str(layer)
                object_list['level-file'][i][1] = ','.join(ojs)
        database.collection('Collabs').document(level).update(object_list)
    
    def delete_object(self, level: str, object_id: int):
        object_list = database.collection('Collabs').document(level).get().to_dict()
        for i in object_list:
            if i['level-file'][0] == object_id:
                object_list['level-file'].remove(object_list['level-file'][i])
        database.collection('Collabs').document(level).update(object_list)
    
    def set_object_attrabute(self, key: int, value, level: str, object_id: int):
        object_list = database.collection('Collabs').document(level).get().to_dict()
        for i in object_list:
            if i['level-file'][0] == object_id:
                object_list['level-file'][i][1] = devutils.strcat(object_list['level-file'][i][1], f'{str(key)}{str(value)}')


class CollabPage:
    def __init__(self): ...
    
    def create_collab(self, collab_name: str, collab_desc: str):
        collab_dict = {
            "description": collab_desc,
            "joined_players": [],
            "level-file": [],
            "level-settings": [],
            "online": [],
            "roles": []
        }
        database.collection('Collabs').document(collab_name).set(collab_dict)
    
    def create_role(self, rolename: str, permitions: str, collab: str):
        collab_dict = database.collection('Collabs').document(collab).get().to_dict()
        collab_dict['roles'].append([rolename, permitions])
        database.collection('Collabs').document(collab).set(collab_dict)
    
    def assign_role(self, role: str, player: str, collab: str):
        collab_dict = database.collection('Collabs').document(collab).get().to_dict()
        for i in enumerate(collab_dict['joined_players']):
            if i[1][1] == player:
                collab_dict[i[0]] = [role, player]
        database.collection('Collabs').document(collab).set(collab_dict)
    
    def set_description(self, description: str, collab: str):
        database.collection('Collabs').document(collab).update({'description': description})
    
    def become_online(self, collab: str):
        online = database.collection('Collabs').document(collab).get().to_dict()['online']
        database.collection('Collabs').document(collab).update({'online': online.append(settings.user_settings.username)})
    
    def become_offline(self, collab: str):
        online = database.collection('Collabs').document(collab).get().to_dict()['online']
        database.collection('Collabs').document(collab).update({'online': online.remove(settings.user_settings.username)})
    
    def download_level(self, collab: str):
        collab_dict = database.collection('Collabs').document(collab).get().to_dict()
        __settings_str = ''.join(collab_dict['level-settings'])
        __level_str = ''.join(collab_dict['level-string'])
        __main_str = ''.join(__settings_str, __level_str)
        main = build.encode_level(__main_str.encode())
        devutils.quick_write(f'collab/{collab}.dat', main, 'wb')

def check_internet_connection() -> bool:
    try:
        requests.get('https://google.com')
        return True
    except requests.ConnectionError:
        return False