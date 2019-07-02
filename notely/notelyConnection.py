# TODO: login, signup, logout
# TODO: get note, add note, update note
# TODO: get folder list, add folder, get folder contents
# TODO: delete folder, delete note
# TODO: make session before request
import requests
import json

session_server = requests.session()

url_server = "http://127.0.0.1:8000/accounts/"


def login_user(username, password):
    server_res = session_server.get(url_server + "login/")
    if 'csrftoken' in server_res.cookies:
        csrf_token = server_res.cookies['csrftoken']
    else:
        csrf_token = 'null'
    dict_login = {'InUsername': username, 'InPassword': password, 'csrfmiddlewaretoken': csrf_token}
    res = session_server.post(url_server + "login/", data=json.dumps(dict_login), headers=dict({"Referer": (url_server + "login/")}))
    if res.status_code == 401:
        # print(res.json())
        print("wht")
        return False
    elif res.status_code == 200:
        # print(res.content)
        print('noway')
        return True
    else:
        print(res.status_code)
        # print(res.content)
        return False
