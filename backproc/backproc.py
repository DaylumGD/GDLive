from win10toast import ToastNotifier
import jsonapis
import firebase_admin
from firebase_admin.credentials import Certificate
from firebase_admin.firestore import client

credentials = Certificate('json/firebase.json')
app = firebase_admin.initialize_app(credentials, name='GDLive')
database = client(app)
json = jsonapis.load_json_file('backproc/settings.json')

class NotificationLib:
    def __init__(self): ...
    
    def notify_invite_request(self, user: str, name: str):
        ToastNotifier().show_toast('You have been invited to a collab', f'User "{user}" has invited you to join their collab "{name}"', 'assets/icon.ico')

def main():
    c_save = database.collection('Users').document(json['username']).get().to_dict()['requested_collabs']
    while True:
        if json['notifications']['invite_requests'] == True:
            save = database.collection('Users').document(json['username']).get().to_dict()['requested_collabs']
            if not c_save == save:
                try:
                    NotificationLib().notify_invite_request(save[len(save)-1]['user'], save[len(save)-1]['collab'])
                    c_save = save
                except: ...

if __name__ == '__main__':
    main()