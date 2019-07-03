# TODO: signup, logout
# TODO: get note, add note, update note
# TODO: get folder list, add folder, get folder contents
# TODO: delete folder, delete note
# TODO: make session before request
import requests
import json

session_server = requests.session()

url_server = "http://127.0.0.1:8000/accounts/"

server_res = session_server.get(url_server + "login/")
if 'csrftoken' in server_res.cookies:
    csrf_token = server_res.cookies['csrftoken']
else:
    csrf_token = 'null'


def send_request(url_page, dict_data, type):
    headers = {'Content-type': 'application/json', "X-CSRFToken": csrf_token, "Referer": (url_server + url_page)}
    dict_data['csrfmiddlewaretoken'] = csrf_token
    if type is "POST":
        return session_server.post(url_server + url_page, data=json.dumps(dict_data), headers=headers)
    elif type is "GET":
        return session_server.get(url_server + url_page, data=json.dumps(dict_data), headers=headers)
    else:
        print("No type other than GET or POST is supported yet")


def login_user(username, password):
    res = send_request("login/", {"InUsername": username, "InPassword": password}, "POST")
    if res.status_code == 401:
        print(res.text)
        return False
    elif res.status_code == 200:
        print(res.text)
        return True
    else:
        print(res.status_code)
        print(res.text)
        return False

